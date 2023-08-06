import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yamlpath",
    version="1.2.2",
    description="Generally-useful YAML and EYAML tools employing a human-friendly YAML Path",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="https://github.com/wwkimball/yamlpath",
    author="William W. Kimball, Jr., MBA, MSIS",
    author_email="github-yamlpath@kimballstuff.com",
    license="ISC",
    keywords="yaml eyaml",
    packages=setuptools.find_packages(),
    scripts=[
        "bin/eyaml-rotate-keys",
        "bin/yaml-get",
        "bin/yaml-set",
    ],
    install_requires=[
        "ruamel.yaml",
    ],
    tests_require=["pytest"],
    include_package_data=True,
    zip_safe=False
)
