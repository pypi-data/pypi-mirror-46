from setuptools import setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="tszip",
    description="Compression utilities for tree sequences",
    long_description=long_description,
    packages=["tszip"],
    author="Tskit Developers",
    author_email="jerome.kelleher@well.ox.ac.uk",
    url="http://pypi.python.org/pypi/tszip",
    setup_requires=['setuptools_scm'],
    install_requires=[
        "numpy",
        "humanize",
        "tskit",
        "numcodecs",
        "zarr",
    ],
    keywords=["Tree sequences", "tskit"],
    license="MIT",
    platforms=["POSIX", "Windows", "MacOS X"],
    python_requires=">=3.4",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    project_urls={
        'Bug Reports': 'https://github.com/tskit-dev/tszip/issues',
        'Source': 'https://github.com/tskit-dev/tszip',
    },
    entry_points={
        'console_scripts': [
            'tszip=tszip.cli:tszip_main',
            'tsunzip=tszip.cli:tsunzip_main',
        ]
    },
    use_scm_version={"write_to": "tszip/_version.py"},
)
