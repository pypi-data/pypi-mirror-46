from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="richprompt",
        version="0.0.1",
        url="https://github.com/lewisacidic/richprompt",
        author="Rich Lewis",
        author_email="opensource@richlew.is",
        description="A better IPython prompt",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        license="MIT",
        keywords=["ipython", "prompt"],
        packages=find_packages(),
        install_requires=["ipython"],
    )
