import setuptools

with open("../../README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="qasdadp",
    version="1.0.3",
    author="Volker Weißmann",
    author_email="volker.weissmann@gmx.de",
    description="The qasdad launcher script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/volkerweissmann/qasdad",
    packages=setuptools.find_packages(),
    install_requires=["qasdad"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
)
