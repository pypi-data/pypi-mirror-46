from setuptools import setup, find_packages

setup(
    name='MakeLog',
    version='0.1a.dev',
    author='Darryl lane',
    author_email='DarrylLane101@gmail.com',
    include_package_data=True,
    license='LICENSE',
    description='''
    Simple logger for info, error and debug
    ''',
    long_description=open('README.md').read(),
    
    scripts=['make_log.py']
)

