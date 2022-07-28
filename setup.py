import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gsnlib",
    version="0.0.1",
    author="Greger Stolt Nilsen",
    author_email="gregersn@gmail.com",
    description="A package of functions I use in my projects",
    long_description=long_description,
    url="http://gregerstoltnilsen.net/",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operation System :: OS Independent"
    ],
    python_required=">=3.6",
    package_data={
        'gsnlib': ['py.typed']
    }
)
