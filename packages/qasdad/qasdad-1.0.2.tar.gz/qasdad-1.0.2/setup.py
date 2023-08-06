import setuptools

with open("../../README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="qasdad",
    version="1.0.2",
    author="Volker Weißmann",
    author_email="volker.weissmann@gmx.de",
    description="Environment for the qasdad scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/volkerweissmann/qasdad",
    packages=setuptools.find_packages(),
    install_requires=["sympy", "numpy", "scipy", "matplotlib", "latex2sympy"], #"nfft", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
)
