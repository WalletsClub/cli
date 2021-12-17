from setuptools import setup

setup(
    name='cli',
    python_requires='>3.8',
    version='0.1.0',
    packages=['messages'],
    url='www.walletsclub.com',
    license='',
    author='zhixiang.xue',
    author_email='x@walletsclub.com',
    description='Command line tool help you to build, test, and manage your WalletsNet integration.',
    entry_points={
        'console_scripts': [
            'walletsnet = walletsnet:cli',
        ],
    },
)
