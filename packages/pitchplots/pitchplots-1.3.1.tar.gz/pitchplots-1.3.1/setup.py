import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pitchplots",
    version="1.3.1",
    author="Fabian Moss",
    author_email="fabian.moss@epfl.ch",
    description="A package containing representation tools for musical purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DCMLab/pitchplots",
    packages=setuptools.find_packages(),
    package_data={
            'pitchplots': ['data/data_example.mxl', 'data/silence.wav', 'data/midi21.wav',
                           'data/midi22.wav', 'data/midi23.wav', 'data/midi24.wav',
                           'data/midi25.wav', 'data/midi26.wav', 'data/midi27.wav',
                           'data/midi28.wav', 'data/midi29.wav', 'data/midi30.wav',
                           'data/midi31.wav', 'data/midi32.wav', 'data/midi33.wav',
                           'data/midi34.wav', 'data/midi35.wav', 'data/midi36.wav',
                           'data/midi37.wav', 'data/midi38.wav', 'data/midi39.wav',],
    },
    install_requires=['matplotlib>=3.0.1',
                      'pandas>=0.23.4',
                      'numpy>=1.15.3',
                      'moviepy>=1.0.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)