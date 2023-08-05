from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='realtime-aws-secretsmngr',
    version='0.0.6',
    license='TBD',
    author='Vasudevan Palani',
    author_email='vasudevan.palani@gmail.com',
    url='https://github.com/vasudevan-palani/realtime-aws-secretsmngr',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['realtimeawssecretsmngr'],
    install_requires=["appsync-client>=0.0.10","paho-mqtt>=1.4.0"],
    include_package_data=True,
    description="Interface to provide callback or push events when secret is updated in aws",
)
