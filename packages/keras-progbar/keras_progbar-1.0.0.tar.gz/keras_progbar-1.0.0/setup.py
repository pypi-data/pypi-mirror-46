import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="keras_progbar",
    version="1.0.0",
    description="the progbar in keras, separating it to use in pytorch. I didn't write this package, the keras-team did",
    long_description=README,
    long_description_content_type="text/markdown",
    url = 'https://github.com/adamleo/keras_progbar',
    author = 'Adam Liu',
    author_email = 'adamhleo@gmail.com',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["keras_progbar"],
    include_package_data=True,
    install_requires=["numpy"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)