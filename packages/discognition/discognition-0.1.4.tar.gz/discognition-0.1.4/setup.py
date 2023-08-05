from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open('discognition/version.py').read())

setup(
    name='discognition',
    version=__version__,
    description='update mp3 metadata and file/directory names using the discogs api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hdbhdb/discognition",
    author='Hudson Bailey',
    author_email='hudsondiggsbailey@gmail.com',
    license='MIT',
    packages=['discognition'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'mutagen>=1.41.1',
        'discogs_client>=2.2.2',
    ],
    scripts=['bin/discognition'],
    zip_safe=False)
