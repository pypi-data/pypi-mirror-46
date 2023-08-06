import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_oauth2",
    version="1.0.4",
    author="Amine BIZID",
    author_email="amine.bizid@gmail.com",
    description="A simple Outh2 client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='Oauth OKTA Azure AD Authentication Authorization token implicit flow',
    url="https://github.com/aminebizid/simple_oauth2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'cryptography',
        'PyJWT>=1.7.1',
        'Flask'
    ]
)