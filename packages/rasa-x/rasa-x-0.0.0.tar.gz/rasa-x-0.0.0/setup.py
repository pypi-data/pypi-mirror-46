from setuptools import setup
import os

# Get the long description from the README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rasa-x",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        # supported python versions
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
    ],
    version="0.0.0",
    description="Rasa X placeholder package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rasa Technologies GmbH",
    author_email="hi@rasa.com",
    maintainer="Tom Bocklisch",
    maintainer_email="tom@rasa.com",
    license="Apache 2.0",
    keywords="nlp machine-learning machine-learning-library bot bots "
             "botkit rasa conversational-agents conversational-ai chatbot"
             "chatbot-framework bot-framework",
    url="https://rasa.com",
    project_urls={
        "Bug Reports": "https://github.com/rasahq/rasa/issues",
        "Source": "https://github.com/rasahq/rasa",
    },
)

if not os.getenv("OVERRIDE"):
    raise RuntimeError('Please use `pip install rasa-x -i https://pypi.rasa.com/simple` instead to install the rasa-x package')