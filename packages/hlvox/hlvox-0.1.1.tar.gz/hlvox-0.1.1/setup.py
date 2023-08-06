from setuptools import setup, find_packages

long_description = """

Originally intended to create sentences from the word snippets for the
Half Life 1 Vox, this project can take a folder of word audio files and piece
them into sentences that are exported as audio files.

"""

setup(
    name='hlvox',
    version='0.1.1',
    author='Blair Hagen',
    packages=find_packages(),
    license='MIT License',
    description='Pieces together voice files to form sentences.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/bhagen/hlvox",
    # long_description=open('README.txt').read(),
    install_requires=[
        "pydub >= 0.23.1",
        "tinydb >= 3.13",
    ],
)
