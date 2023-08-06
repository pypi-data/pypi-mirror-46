from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    version='0.0.3',
    name='repostatus',
    packages=['repostatus'],
    description='Python module for managing github repo status',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Tony Vattathil',
    author_email='avattathil@gmail.com',
    url='https://avattathil.github.io/repostatus',
    license='Apache License 2.0',
    download_url='https://github.com/avattathil/repostatus/tarball/master',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Operating System :: POSIX :: Linux',
    ],
    scripts=[
        'bin/repostatus'
    ],
    keywords=['git', 'repostatus'],
    install_requires=required,
#    test_suite="tests",
#    tests_require=["mock", "boto3"],
    include_package_data=True
)
