from setuptools import setup

setup(name='hadir',
	version='0.5',
	description='Recursively hash directory trees for checking backups.',
	author='Jori Niemi',
	license='MIT',
	packages=['hadir'],
	zip_safe=False,
	entry_points = {
        'console_scripts': ['hadir=hadir.hasher:main','hadir-diff=hadir.differ:main'],
    },
    python_requires=">=3.2"
)