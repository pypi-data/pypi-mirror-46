import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sequence_field",
    version="v1.0.4",
    author="Alan Zhang",
    author_email="1095087479@qq.com",
    description="flask sqlalchemy sequence field",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['sequence_field'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'SQLAlchemy',
    ],

)