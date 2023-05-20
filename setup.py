from setuptools import setup

setup(
    name="inverted_index",
    version="0.1",
    package_dir={"inverted_index": "src"},
    install_requires=[
        "pandas",
        "tqdm",
        "nltk",
        "pymorphy2",
    ],
)
