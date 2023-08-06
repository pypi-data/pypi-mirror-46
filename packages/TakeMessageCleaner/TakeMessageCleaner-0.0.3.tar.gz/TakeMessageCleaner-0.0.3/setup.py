import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()	

setuptools.setup(
    name="TakeMessageCleaner",
    version="0.0.3",
    author="Karina Tiemi Kato",
    author_email="karinatkato@gmail.com",
    description="TakeMessageCleaner is a tool for pre processing messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karinatk/TakeMessageCleaner",
    packages=setuptools.find_packages(),
	install_requires=requirements,
	package_data = {
		'dictionaries': ['*.json'],
	},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)