from setuptools import setup

with open("LICENSE", "r") as fh:
    license = fh.read()

with open("README.md") as rm:
    long_description = rm.read()

setup(
    name='rlock',
    version='0.0.5',
    install_requires=['requests'],
    python_requires='~=3.7',
    packages=['rlock'],
    url='https://github.com/cloudcraeft/rlock',
    license=license,
    author='cloudcraeft',
    author_email='cloudcraeft@outlook.com',
    description='A RedLock API Client',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
