from distutils.core import setup

setup(
    name='FFIG',
    version='0.0.dev',
    packages=['ffig','ffig/clang', 'ffig/filters'],
    license='MIT license',
    long_description=open('README.md').read(),
    url='http://ffig.org',
    package_data={'FFIG': ['ffig/templates/*']}
)
