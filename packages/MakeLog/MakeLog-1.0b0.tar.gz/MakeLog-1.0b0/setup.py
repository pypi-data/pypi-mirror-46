from setuptools import setup, find_packages

setup(
    name='MakeLog',
    version='1.0b',
    author='Darryl lane',
    author_email='DarrylLane101@gmail.com',
    packages=['MakeLog'],
    include_package_data=True,
    license='LICENSE',
    description='''
    Simple logger for info, error and debug
    ''',
    long_description=open('README.md').read(),
    
    scripts=['MakeLog/make_log.py']
)

