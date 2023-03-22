from setuptools import setup, find_packages

__version__ = "0.0.2"

# More information on setting values:
# https://github.com/Sceptre/project/wiki/sceptre-resolver-template

# lowercase, use `-` as separator.
RESOLVER_NAME = "sceptre-request-resolver"
# the resolver call in sceptre e.g. !command_name.
RESOLVER_COMMAND_NAME = "request"
# do not change. Rename resolver/resolver.py to resolver/{RESOLVER_COMMAND_NAME}.py
RESOLVER_MODULE_NAME = "resolver.{}".format(RESOLVER_COMMAND_NAME)
# CamelCase name of resolver class in resolver.resolver.
RESOLVER_CLASS = "Request"
# One line summary description
RESOLVER_DESCRIPTION = "A Sceptre resolver to make requests from REST API endpoints"
# if multiple use a single string with comma separated names.
RESOLVER_AUTHOR = "zaro0508"
# if multiple use single string with commas.
RESOLVER_AUTHOR_EMAIL = "sceptreorg@gmail.com"
RESOLVER_URL = "https://github.com/sceptre/{}".format(RESOLVER_NAME)

with open("README.md") as readme_file:
    README = readme_file.read()

install_requirements = ["sceptre>=3.2", "validator-collection>=1.5"]

test_requirements = [
    "pytest>=6.2",
]

setup_requirements = ["pytest-runner>=6.0"]

setup(
    name=RESOLVER_NAME,
    version=__version__,
    description=RESOLVER_DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    author=RESOLVER_AUTHOR,
    author_email=RESOLVER_AUTHOR_EMAIL,
    license="Apache2",
    url=RESOLVER_URL,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    py_modules=[RESOLVER_MODULE_NAME],
    entry_points={
        "sceptre.resolvers": [
            "{}={}:{}".format(
                RESOLVER_COMMAND_NAME, RESOLVER_MODULE_NAME, RESOLVER_CLASS
            )
        ]
    },
    include_package_data=True,
    zip_safe=False,
    keywords="sceptre, sceptre-resolver",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Environment :: Console",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    test_suite="tests",
    install_requires=install_requirements,
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    extras_require={"test": test_requirements},
)
