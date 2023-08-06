import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='crlint',
    version='0.0.1',
    author='Celadon Team',
    author_email='opensource@celadon.ae',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/celadonteam/crtool',
    packages=[
        'crlint',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'crlint=crlint.__main__:main',
        ],
    },
)
