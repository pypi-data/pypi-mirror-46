from distutils.core import setup

setup(
    name='ybc_agent',
    version='1.0.2',
    description='agent that should be install into sandbox',
    long_description='the agent will connect to agent server via websocket, get messages from websocket and process them',
    author='lanbo',
    author_email='lanbo@fenbi.com',
    keywords=['pip3', 'python3', 'python'],
    url='http://pip.zhenguanyu.com/',
    packages=['ybc_agent'],
    package_data={'ybc_agent': ['*.py']},
    license='MIT',
    install_requires=[
        'ybc_config',
        'websocket_client'
    ],
)
