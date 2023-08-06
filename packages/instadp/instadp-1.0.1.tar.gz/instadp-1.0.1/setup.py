import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='instadp',
    version='1.0.1',
    author='Siddharth Dushantha',
    author_email='siddharth.dushantha@gmail.com',
    description='Download any users Instagram display picture/profile picture in full quality',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sdushantha/instadp',
    packages=setuptools.find_packages(),
    scripts=['instadp/instadp'],
    install_requires=['requests']
)

