import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="preprocessRawText",
    version="0.0.24",
    author="nguyentho",
    author_email="nguyentho0207@gmail.com",
    description="preprocessRawText NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nguyenthohy/preprocess.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],

    package_data={
            'preprocessRawText': ['vietnamese-stopwords-dash.txt']
        },

    install_requires=['flashtext', 'gensim', 'pyvi'],

)
