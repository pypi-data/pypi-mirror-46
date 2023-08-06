from setuptools import setup

setup(
    name='isplogger',
    version='0.2.0',
    description='A tool for monitoring/recording internet access',
    url='http://github.com/tjkessler/isplogger',
    author='Travis Kessler',
    author_email='travis.j.kessler@gmail.com',
    license='MIT',
    packages=['isplogger'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'isp-logger=isplogger.cmd_line:main'
        ]
    },
    zip_safe=False
)
