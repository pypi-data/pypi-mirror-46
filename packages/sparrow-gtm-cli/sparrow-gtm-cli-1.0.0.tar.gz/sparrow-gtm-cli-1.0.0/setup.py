from setuptools import setup
import setuptools

setup(
    name='sparrow-gtm-cli',
    packages=setuptools.find_packages(),
    version='1.0.0',
    description='Google GTM Wrapper',
    license='GPLv3',
    author='Fady F Salem',
    author_email='ffaried@talabat.com',
    download_url='https://github.com/fadyfaried/sparrow-gtm-cli',
    keywords=['gtm', 'sparrow-cli'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
    ],
    entry_points={
        'console_scripts': [
            'sparrow = sparrow.cli:main',
        ],
    }
)
