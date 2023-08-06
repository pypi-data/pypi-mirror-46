import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="syntactic_tagger",
                 version="1.0.1",
                 author="Ivan Arias Rodriguez",
                 author_email="ivansiiito@gmail.com",
                 description="Spanish part-of-speech tagger using a syntactic table.",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/ivansiiito/syntactic_tagger",
                 packages=setuptools.find_packages(),
                 classifiers=["Programming Language :: Python :: 3",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent",
                              ],
                 )
