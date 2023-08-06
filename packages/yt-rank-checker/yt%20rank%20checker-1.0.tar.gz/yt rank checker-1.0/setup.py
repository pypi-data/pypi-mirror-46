from setuptools import setup, find_packages

setup(
    name='yt rank checker',
    version='1.0',
    author='Renaissance Troll',
    author_email='troll@renaissancetroll.com',
    packages=['yt_rank_checker'],
    license='LICENSE.txt',
    description='Find where videos rank on YouTube by keywords for a youtube channel',
    install_requires=['arrow==0.12.1','selenium == 3.12','pyecharts==1.0.0']

)