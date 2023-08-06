from setuptools import setup, find_packages

from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ucam-wls',
    version='0.0.2',
    author="Edwin Bahrami Balani",
    author_email="eb677@srcf.net",
    license="MIT",
    description="A web login service library for the Ucam-WebAuth (WAA2WLS) protocol",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url="https://github.com/edwinbalani/ucam-wls",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        'cryptography',
    ],
    python_requires='>=3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
    keywords="cambridge university raven login authentication waa2wls ucam "
             "webauth ucam-webauth wls",
)
