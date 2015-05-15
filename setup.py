from setuptools import setup


setup(
    name='throttledsocket',
    version='0.0.1',
    author="Ashish Dubey",
    author_email="ashish.dubey91@gmail.com",
    packages=['throttledsocket', ],
    license='MIT',
    long_description='Socket wrapper for rate limited network I/O.',
    install_requires=['gevent', ],
)
