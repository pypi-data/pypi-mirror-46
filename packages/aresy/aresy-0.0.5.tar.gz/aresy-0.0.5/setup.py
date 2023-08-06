import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aresy",
    version="0.0.5",
    author="Zhengyang Tang",
    author_email="zytang7@gmail.com",
    description="An industrial-strength data science toolkits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tangzhy/aresy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
