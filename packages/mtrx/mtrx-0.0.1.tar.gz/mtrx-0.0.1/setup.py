import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mtrx",
    version="0.0.1",
    author="Mostafa Vahedi Nejad",
    author_email="mostafa.vahedi.nejad@gmail.com",
    description="A Python ToolBox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mostafa-vn/mtrx",
    packages=setuptools.find_packages(),
    keywords="mtrx mostafa matrix python v3",
    install_requires=['requests', 'pyqrcode'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
	'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
