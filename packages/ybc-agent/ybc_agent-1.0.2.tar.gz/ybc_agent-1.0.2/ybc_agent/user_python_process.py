import argparse
import errno
import os
import pwd
import subprocess
import shlex

from enum import IntEnum
from singleton import Singleton


env_dict = {}


def set_user(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)

    return result


def mkdir_p(path):
    if not path:
        return
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class StoreDictKeyPair(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super(StoreDictKeyPair, self).__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        for kv in values:
            k, v = kv.split("=")
            env_dict[k] = v
        setattr(namespace, self.dest, env_dict)


class Parser(metaclass=Singleton):

    def __init__(self):
        parser = argparse.ArgumentParser(description='YBC exec tool')
        parser.add_argument("--env", dest="env_dict", action=StoreDictKeyPair, nargs="+", metavar="KEY=VAL")
        parser.add_argument("--working-dir")
        parser.add_argument("--user")
        parser.add_argument("--stdout")
        parser.add_argument("--stderr")
        parser.add_argument("--pid-file")
        parser.add_argument("--exit-code-file")
        parser.add_argument("--command")
        parser.add_argument("--tag")
        self.parser = parser

    def parse_args(self, args):
        return self.parser.parse_args(args)


class Command:
    def __init__(self, args):
        parser = Parser()
        args = parser.parse_args(args)
        user_name = args.user
        pw_record = pwd.getpwnam(user_name)
        user_name = pw_record.pw_name
        user_home_dir = pw_record.pw_dir
        self.uid = pw_record.pw_uid
        self.gid = pw_record.pw_gid

        self.working_directory = args.working_dir
        self.stdout_file = args.stdout or ""
        self.stderr_file = args.stderr or ""
        self.pid_file = args.pid_file or ""
        self.exitcode_file = args.exit_code_file or ""
        self.command = args.command or ""
        self.tag = args.tag or ""

        env_dict['HOME'] = user_home_dir
        env_dict['LOGNAME'] = user_name
        env_dict['PWD'] = self.working_directory
        env_dict['USER'] = user_name
        env_dict['LANG'] = 'en_US.utf8'

        if 'YBC_REQUEST_FILE' in env_dict:
            env_dict['YBC_REQUEST_FILE'] = '/sandbox/' + env_dict['YBC_REQUEST_FILE']

        if 'YBC_RESPONSE_FILE_PREFIX' in env_dict:
            env_dict['YBC_RESPONSE_FILE_PREFIX'] = '/sandbox/' + env_dict['YBC_RESPONSE_FILE_PREFIX']

        env_dict['YBC_STDOUT_FILE'] = self.stdout_file
        env_dict['YBC_STDERR_FILE'] = self.stderr_file


class UserPythonProcessStatus(IntEnum):
    INIT = 0
    RUNNING = 1
    FINISHED = 2
    KILLED = -1
    EXCEPTION = -2
    ERROR = -3


class UserPythonProcess(object):

    def __init__(self, command: Command, on_open, on_exit, on_error):
        self.command = command.command
        self.stdout_file = command.stdout_file
        self.stderr_file = command.stderr_file
        self.env_dict = env_dict
        self.working_directory = command.working_directory
        self.pid_file = command.pid_file
        self.exitcode_file = command.exitcode_file
        self.uid = command.uid
        self.gid = command.gid
        self.on_open = on_open
        self.on_exit = on_exit
        self.on_error = on_error
        self.process = None
        self.status = UserPythonProcessStatus.INIT
        self.tag = command.tag

    def run(self):
        mkdir_p(os.path.dirname(self.stdout_file))
        mkdir_p(os.path.dirname(self.stderr_file))
        open(self.stdout_file, 'w+').close()
        open(self.stderr_file, 'w+').close()

        try:
            self.process = subprocess.Popen(
                shlex.split(self.command),
                env=self.env_dict,
                cwd=self.working_directory,
                shell=False,
                preexec_fn=set_user(self.uid, self.gid)
            )
        except OSError as ex:
            self.status = UserPythonProcessStatus.ERROR
            if self.on_error and callable(self.on_error):
                self.on_error(self)
            return

        self.status = UserPythonProcessStatus.RUNNING
        if self.on_open and callable(self.on_open):
            self.on_open(self)

        with open(self.pid_file, "w+") as f:
            f.write(str(self.process.pid))

        self.process.wait()

        with open(self.exitcode_file, "w") as f:
            f.write(str(self.process.returncode))

        returncode = self.process.returncode
        if returncode == -9:
            # SIGKILL
            self.status = UserPythonProcessStatus.KILLED
        elif returncode == -15:
            # SIGTERM
            self.status = UserPythonProcessStatus.KILLED
        elif returncode == 0:
            self.status = UserPythonProcessStatus.FINISHED
        else:
            # TODO: 负数值的情况可能是有异常情况，暂不处理
            self.status = UserPythonProcessStatus.EXCEPTION

        if self.on_exit and callable(self.on_exit):
            self.on_exit(self)

    def kill(self):
        if self.process:
            self.process.kill()

    def pid(self):
        if self.process:
            return self.process.pid

    def return_code(self):
        if self.process:
            return self.process.returncode