from setuptools import setup, find_packages


def read(file_name):
    with open(file_name) as fp:
        content = fp.read()
    return content


setup(
    name="marshmallow-dumped-order",
    version="1.0.0",
    description="Decorator for `marshmallow.Schema` to sort fields "
                "in needed order while dumping",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_dir={'marshmallow-dumped-order': 'marshmallow-dumped-order'},
    author="Danilchenko Maksim",
    author_email="dmax.dev@gmail.com",
    include_package_data=True,
    install_requires=read("requirements.txt").split(),
    license="MIT",
    url="https://github.com/maximdanilchenko/marshmallow-dumped-order",
    zip_safe=False,
    keywords="marshmallow schema dump fields order",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    test_suite="tests",
)
