import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="pmg",
    version="0.0.0",
    author="Preston Meyer Group",
    author_email="dev@pmgroup.ch",
    description="PMG toolbox",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=open('requirements.txt', 'r').read(),
    python_requires='~=3.6',
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
