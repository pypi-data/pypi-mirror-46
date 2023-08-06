import setuptools

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

install_and_import('webbrowser')
install_and_import('mistune')
import mistune

with open("README.md", "r") as fh:
    long_description = mistune.markdown(fh.read())

setuptools.setup(
    name="Mark2PY",
    version="0.5",
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
