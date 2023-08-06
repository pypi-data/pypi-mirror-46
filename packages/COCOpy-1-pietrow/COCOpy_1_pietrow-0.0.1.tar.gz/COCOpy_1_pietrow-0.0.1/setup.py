import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
                 name="COCOpy_1_pietrow",
                 version="0.0.1",
                 author="A.G.M. Pietrow",
                 author_email="Alex.pietrow@astro.su.se",
                 description="COlor COllapsed Plotting software",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/AlexPietrow/COCO/tree/master/Python",
                 packages=setuptools.find_packages(),
                 classifiers=[
                              "Programming Language :: Python :: 2.7",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent",
                              ],
                 )
