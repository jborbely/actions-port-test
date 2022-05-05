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
    install_requires=[
        'msl-loadlib @ git+https://github.com/MSLNZ/msl-loadlib.git',
        'comtypes;sys_platform=="win32"',
        'py4j',
        'pythonnet; python_version<="3.8"',
        'pythonnet @ git+https://github.com/pythonnet/pythonnet.git@ac75e0ccc31c2780b57c01fe134652f1f1b90466; python_version>"3.8"'
    ],
    include_package_data=True,
)
