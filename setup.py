import sys

from setuptools import setup

install_requires = [
    'msl-loadlib @ git+https://github.com/MSLNZ/msl-loadlib.git',
    'py4j',
]

if sys.platform == 'win32':
    install_requires.append('comtypes')

if sys.version_info[:2] <= (3, 8):
    if sys.platform == 'darwin' and sys.version_info[:2] <= (3, 5):
        pass
    else:
        install_requires.append('pythonnet')
else:
    install_requires.append('pythonnet @ git+https://github.com/pythonnet/pythonnet.git@ac75e0ccc31c2780b57c01fe134652f1f1b90466')


setup(
    name='actions',
    version='0.1.0',
    author='me',
    author_email='me@home',
    description='GA port issue',
    url='actions-port-test',
    entry_points={'console_scripts': ['run-server = actions:run']},
    packages=['actions'],
    install_requires=install_requires,
    include_package_data=True,
)
