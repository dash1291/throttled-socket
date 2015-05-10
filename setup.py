from distutils.core import setup

setup(
    name='throttledsocket',
    version='0.0.1',
    packages=['throttledsocket',],
    license='MIT',
    long_description='Socket wrapper for rate limited network I/O.',
    install_requires=['gevent',],
)
