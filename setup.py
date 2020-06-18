import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="raynigon-smime-generator",
    version="0.0.1",
    author="Simon Schneider",
    author_email="10846939+raynigon@users.noreply.github.com",
    description="Easy SMIME Certificate Handling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raynigon/smime-generator",
    scripts=['scripts/cert_generator.py'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",        
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)