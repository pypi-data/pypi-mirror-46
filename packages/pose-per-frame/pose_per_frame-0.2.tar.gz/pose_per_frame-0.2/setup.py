import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pose_per_frame",
    version="0.2",
    author="Rafael RazorLabs",
    author_email="rafael@razor-labs.com",
    description="get pose prediction, given a frame and a model",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ],
)