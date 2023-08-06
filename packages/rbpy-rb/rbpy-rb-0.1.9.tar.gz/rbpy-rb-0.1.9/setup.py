import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rbpy-rb',
    version='0.1.9',
    author='Woodcarver',
    author_email='batpepastrama@gmail.com',
    description='ReaderBench library written in python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://git.readerbench.com/ReaderBench/Readerbench-python',
    packages=setuptools.find_packages(),
    dependency_links=['https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz'],
    install_requires=[
          'wheel',
          'spacy>=2.1',
          'nltk',
          'gensim',
          'numpy',
          'wget',
          'pymorphy2',
          'neuralcoref'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
)
