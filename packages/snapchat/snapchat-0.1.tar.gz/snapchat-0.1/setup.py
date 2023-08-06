import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='snapchat',
    version='0.1',
    author='Siddharth Dushantha',
    author_email='siddharth.dushantha@gmail.com',
    description='Unofficial SnapChat API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sdushantha/snapchat',
    packages=setuptools.find_packages(),
    install_requires=['requests']
)
