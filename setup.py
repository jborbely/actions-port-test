from setuptools import setup

setup(
    name='actions',
    version='0.1.0',
    author='me',
    author_email='me@home',
    description='GA port issue',
    url='actions-port-test',
    entry_points={'console_scripts': ['run-server = actions:run']},
    packages=['actions'],
    install_requires=['msl-loadlib @ git+https://github.com/MSLNZ/msl-loadlib.git'],
    include_package_data=True,
)
