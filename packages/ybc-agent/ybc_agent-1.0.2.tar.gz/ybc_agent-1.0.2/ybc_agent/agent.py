import argparse
import json
import logging
import math
import os
import signal
import sys

try:
    import thread
except ImportError:
    import _thread as thread
import threading
import time
import websocket


from enum import IntEnum
from daemon import Daemon
from user_python_process import UserPythonProcess, Command, UserPythonProcessStatus
from ybc_config import config

__WEBSOCKET_PING_INTERVAL__ = 25

if sys.platform == 'darwin':
    __PID_FILE_ = "/usr/local/var/run/sandbox/agent.pid"
    __STDOUT_LOG_FILE_ = "/usr/local/var/log/sandbox/agent.log"
    __STDERR_LOG_FILE_ = "/usr/local/var/log/sandbox/agent.err.log"
else:
    __PID_FILE_ = "/var/run/sandbox/agent.pid"
    __STDOUT_LOG_FILE_ = "/var/log/sandbox/agent.log"
    __STDERR_LOG_FILE_ = "/var/log/sandbox/agent.err.log"

FORMAT = "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)s:%(funcName)s()] %(message)s"
logging.basicConfig(filename=__STDOUT_LOG_FILE_, level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)


class MessageType(IntEnum):
    PING = 0
    PONG = 1
    EXEC = 2
    KILL = 3
    STATUS = 4
    BAD_EXEC = 5


class Message:
    def __init__(self, type, timestamp, payload=None):
        self.type = type
        self.timestamp = timestamp
        if payload is not None:
            self.payload = self._deserialize_payload(type, payload)

    @staticmethod
    def _deserialize_payload(type, payload):
        if type == MessageType.EXEC.value:
            return ExecRequest(**payload)


class ExecRequest:
    _INVALID_PROCESS_ID_ = -1
    _INVALID_REQUEST_ID_ = -1

    def __init__(self, processId, args):
        """
        :param id: id of the request
        :param processId: id of the sandbox process
        :param args: command args
        """
        self.processId = processId
        self.args = args


class BadExecRequestReason(IntEnum):
    REQUEST_UNKNOWN = 1
    REQUEST_REPEAT = 2
    REQUEST_BAD_ARGS = 3


class BadExecRequest(Exception):
    def __init__(self, reason: BadExecRequestReason):
        self.reason = reason


class WebsocketClient(object):

    def __init__(self, token, on_open, on_message, on_error, on_close):
        url = "%s?token=%s" % (config['websocket'], token)
        logger.info("Creating websocket client: url=%s" % url)
        self.ws = websocket.WebSocketApp(url,
                                         on_message=on_message,
                                         on_error=on_error,
                                         on_close=on_close)
        self.ws.on_open = on_open
        self.is_connected = False

    def run(self):
        logger.info("Start websocket client...")
        self.ws.run_forever()


class AgentDaemon(Daemon):
    """
    The agent daemon. Will do such work:
    1. Create and manage websocket connection.
    2. Manage python process of user

    Now a user can run only one python process at the same time
    """

    def __init__(self, token, pid_file, stdout, stderr):
        def _on_open(ws):
            self.client_used = True
            self.reconnect_count = 0
            self.reconnect_wait = 1
            self.client.is_connected = True

            if os.path.exists('/proc/%d' % self.ppid):
                os.kill(self.ppid, signal.SIGUSR1)

            logger.info("Websocket connected")

            def _send_ping(*args, interval=25):
                logger.info("Begin sending heartbeat: interval=%d, threadIdentifier=%d" % (interval, threading.current_thread().ident))
                tls = threading.local()
                if not hasattr(tls, 'client'):
                    tls.client = self.client
                while ws and self.client and tls.client is self.client:
                    message = {
                        'type': 0,
                        'timestamp': time.time() * 1000
                    }
                    _do_send(message)
                    time.sleep(interval)

                logger.info("Thread terminating: threadIdentifier=%d" % threading.current_thread().ident)
                ws.close()

            thread.start_new_thread(_send_ping, (__WEBSOCKET_PING_INTERVAL__,))

        def _on_close(ws):
            logger.info("### Websocket closed ###")
            self.client.is_connected = False
            _reconnect()

        def _on_message(ws, message):
            logger.info("Got message: %s" % message)
            try:
                _process_message(_decode_message(message))
            except Exception as e:
                logger.error(e)

        def _on_error(ws, error):
            logger.error(error)
            if os.path.exists('/proc/%d' % self.ppid):
                os.kill(self.ppid, signal.SIGUSR2)

        def _reconnect():
            logger.info("Websocket reconnecting: reconnectCount=%d" % self.reconnect_count)
            if not self.rlock.acquire(blocking=False):
                return
            if not self.client.is_connected:
                self.reconnect_count += 1
                self.reconnect_wait *= 2
                time.sleep(self.reconnect_wait)
                if self.client_used:
                    self.client = WebsocketClient(token, _on_open, _on_message, _on_error, _on_close)
                self.client.run()
            self.rlock.release()

        def _decode_message(message):
            try:
                return Message(**json.loads(message))
            except Exception as e:
                logger.error(e)

        def _do_exec(message: Message):
            exec_request = message.payload
            if not isinstance(exec_request, ExecRequest):
                return BadExecRequest(BadExecRequestReason.REQUEST_UNKNOWN)

            if self.current_user_python_process:
                raise BadExecRequest(BadExecRequestReason.REQUEST_REPEAT)

            # 加锁，同一时间只允许用户运行一个程序
            if not self.rlock.acquire(timeout=0.05):
                raise BadExecRequest(BadExecRequestReason.REQUEST_REPEAT)

            # double check
            if not self.current_user_python_process:
                self.current_process_id = int(exec_request.processId)
                try:
                    command = Command(exec_request.args)
                    self.current_user_python_process = UserPythonProcess(command,
                                                                         _on_student_python_process_open,
                                                                         _on_student_python_process_exit,
                                                                         _on_student_python_process_error)
                    thread.start_new_thread(self.current_user_python_process.run, ())
                except Exception:
                    self.rlock.release()
                    raise BadExecRequest(BadExecRequestReason.REQUEST_BAD_ARGS)
            else:
                self.rlock.release()
                raise BadExecRequest(BadExecRequestReason.REQUEST_REPEAT)

            self.rlock.release()

        def _do_kill():
            if self.current_user_python_process:
                self.current_user_python_process.kill()

        def _process_message(message: Message):
            if message.type == MessageType.PING.value:
                pass
            elif message.type == MessageType.PONG.value:
                pass
            elif message.type == MessageType.EXEC.value:
                try:
                    _do_exec(message)
                except BadExecRequest as ber:
                    logger.error(ber)
                    message = {
                        'type': MessageType.STATUS,
                        'timestamp': _get_ts_in_milliseconds_now(),
                        'payload': {
                            'processId': self.current_process_id,
                            'pid': -1,
                            'status': UserPythonProcessStatus.ERROR,
                            'returnCode': -1,
                            'tag': self.current_user_python_process.tag
                        }
                    }
                    _do_send(message)
            elif message.type == MessageType.KILL.value:
                _do_kill()

        def _on_student_python_process_open(p: UserPythonProcess):
            logger.info("User process started: pid=%d" % p.pid())
            self.rlock.acquire()
            self.current_user_python_process = p
            _report_process_status()
            self.rlock.release()

        def _on_student_python_process_exit(p: UserPythonProcess):
            logger.info("User process exit: pid=%d, processId=%d" % (p.pid(), self.current_process_id))
            self.rlock.acquire()
            _report_process_status()
            self.current_user_python_process = None
            self.rlock.release()

        def _on_student_python_process_error(p: UserPythonProcess):
            logger.info("Open user process failed: processId=%d" % self.current_process_id)
            self.rlock.acquire()
            _report_process_status()
            self.current_user_python_process = None
            self.rlock.release()

        def _report_process_status():
            message = {
                'type': MessageType.STATUS,
                'timestamp': _get_ts_in_milliseconds_now(),
                'payload': {
                    'processId': self.current_process_id,
                    'pid': self.current_user_python_process.pid(),
                    'status': self.current_user_python_process.status,
                    'returnCode': self.current_user_python_process.return_code(),
                    'tag': self.current_user_python_process.tag
                }
            }
            logger.info("Report process status: %s" % json.dumps(message))
            _do_send(message)

        def _get_ts_in_milliseconds_now():
            return math.ceil(time.time() * 1000)

        def _do_send(message):
            try:
                self.client.ws.send(json.dumps(message))
            except Exception as ex:
                self.client.is_connected = False
                _reconnect()

        def _signal_handler(signal_number, frame):
            if signal_number == signal.SIGUSR1:
                print("success")
                sys.exit(0)
            else:
                print("fail")
                sys.exit(1)

        super().__init__(pid_file, stdin=os.devnull,
                         stdout=stdout, stderr=stderr,
                         home_dir='.', umask=0o22, verbose=1,
                         use_gevent=False, use_eventlet=False)
        self.client = WebsocketClient(token, _on_open, _on_message, _on_error, _on_close)
        self.client_used = False
        self.reconnect_count = 0
        self.reconnect_wait = 1
        self.ping_thread = 0
        self.rlock = threading.RLock()
        self.current_user_python_process = None
        self.current_process_id = ExecRequest._INVALID_PROCESS_ID_
        self.ppid = os.getpid()

        is_parent = self.start(exit_parent_after_fork=False)

        if is_parent:
            signal.signal(signal.SIGUSR1, _signal_handler)
            signal.signal(signal.SIGUSR2, _signal_handler)
            signal.pause()

    def run(self):
        logger.info("Agent daemon is running...")
        try:
            self.client.run()
        except Exception:
            if os.path.exists('/proc/%d' % self.ppid):
                os.kill(self.ppid, signal.SIGUSR2)
            raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YBC agent tool, once started, will run in daemon mode')
    parser.add_argument("--token", required=True)
    args = parser.parse_args()

    daemon = AgentDaemon(args.token, __PID_FILE_, __STDOUT_LOG_FILE_, __STDERR_LOG_FILE_)
