"""pyxlogin setup file."""
from setuptools import find_packages
from setuptools import setup


def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name='pyxlogin',
    version='0.1',
    description='Python telnet client',
    long_description='Telnet/SSH to Linux/UNIX servers and network routers/switches using telnet/ssh and expect commands.',
    license='MIT',
    author='Miyahan',
    author_email='miyahan.com@gmail.com',
    url='https://github.com/miyahan/pyxlogin',
    keywords='telnet xlogin router',
    packages=find_packages(),
    platforms=['POSIX'],
    install_requires=_requires_from_file('requirements.txt'),
    classifires=[
        'Programing Language :: Python :: 3',
        'Programing Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
)
