from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="sna_prediction",
    version="0.1",
    description="A python package to predict outcome of an event based on type of data it is fed to.For now it is Loksabha 2019 Elections",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/itsDevhere/social-network-analysis",
    author="Devpratim Das , Rana Mondal , Souvik Das , Soumyajeet Bose",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"],
    packages=["sna_prediction"],
    include_package_data=True,
    install_requires=["tweepy","textblob","wordcloud","PyQt5","pandas","numpy","networkx==2.3","matplotlib","emoji"],
    entry_points={
        "console_scripts": [
            "sna_prediction=sna_prediction.main:main",
        ]
    },
)