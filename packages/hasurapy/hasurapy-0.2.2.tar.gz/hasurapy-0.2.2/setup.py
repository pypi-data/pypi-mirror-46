import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='hasurapy',
    version='0.2.2',
    author="Chris Nurse",
    author_email="contact@namsource.com",
    description="An enhanced python interface to Hasura",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/namsource_os/hasurapy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
