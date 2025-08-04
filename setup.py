from setuptools import find_packages, setup

setup(
    name="mcqgenerator",
    version="0.0.1",
    author="Gokul Sundeep",
    author_email="gokulsundeep@gmail.com",
    description="A tool to generate multiple choice questions from text",
    install_requires=["openai", "langchain", "streamlit", "python-dotenv", "pyPDF2", "langchain-openai", 
                      "langchain-community"],
    packages=find_packages()
)