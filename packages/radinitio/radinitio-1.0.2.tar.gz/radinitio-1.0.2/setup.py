import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="radinitio",
    version="1.0.2",
    author="Angel G. Rivera-Colon <angelgr2@illinois.edu>, Nicolas Rochette <rochette@illinois.edu>, Julian Catchen <jcatchen@illinois.edu>",
    author_email="angelgr2@illinois.edu",
    description="A package for the simulation of RADseq data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    scripts=['scripts/radinitio'],
    python_requires='>3.5',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux",
    ],
    project_urls={
        'Manual'  : 'http://catchenlab.life.illinois.edu/radinitio/manual/',
        'Website' : 'http://catchenlab.life.illinois.edu/radinitio',
        'Source'  : 'https://bitbucket.org/angelgr2/radinitio/src/default/' },
    install_requires=[
        'scipy',
        'numpy',
        'msprime',
    ],
)
