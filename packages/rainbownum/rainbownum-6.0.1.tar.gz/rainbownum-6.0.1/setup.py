import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rainbownum",
    version="6.0.1",
    author="Simon Wagner",
    author_email="swagner648@gmail.com",
    description="Python package to solve anti-Schur equations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy'
    ]
)

# 1. Change version number
# 2. Run 'python3 setup.py sdist bdist_wheel'
# 3. Run 'python3 -m twine upload dist/*'