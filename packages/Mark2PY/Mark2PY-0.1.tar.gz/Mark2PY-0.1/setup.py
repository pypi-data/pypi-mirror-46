import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Mark2PY",
    version="0.1",
    author="AMJoshaghani",
    author_email="amjoshaghani@gmail.com",
    description="this package help developers to write Markdown & Markup in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amjoshaghani/Mark2PY",
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
