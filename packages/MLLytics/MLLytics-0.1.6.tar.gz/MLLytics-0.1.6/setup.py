from setuptools import setup

VERSION = '0.1.6'

CLASSIFIERS = ['Intended Audience :: Science/Research',
			   'Intended Audience :: Developers',
			   'Programming Language :: Python :: 3',
			   'Topic :: Software Development',
			   'Topic :: Scientific/Engineering',
			   'Operating System :: Microsoft :: Windows',
			   'Operating System :: Unix',
			   'Operating System :: MacOS'
			   ]

setup(
	name='MLLytics',
    version=VERSION,
	packages=['MLLytics'],
    url='https://github.com/scottclay/MLLytics',
	license='MIT',
    author='Scott Clay',
    author_email='scottclay8@gmail.com',
    description='A library of tools for easier evaluation of ML models.',
	long_description=open('README.md').read(),
	install_requires=['numpy >= 1.14.3', 'matplotlib >= 2.2.2', 'seaborn >= 0.8.1', 'pandas >= 0.23.0',
					'scikit-learn >= 0.19.1'],
    zip_safe=False,
	classifiers = CLASSIFIERS
	)