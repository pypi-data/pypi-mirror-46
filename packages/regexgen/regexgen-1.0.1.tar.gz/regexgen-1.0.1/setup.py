from setuptools import setup, find_packages

setup(
    name = 'regexgen',
    version = '1.0.1',
    description = 'Turn list of strings to minimal regex. Also supports turning a list of string into a minimal grouped expression. ',
    url = '', # git link here
    author = 'Jo-Frederik Krohn',
    author_email='jo-frederik.krohn@accenture.com',
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
        ],
    keywords = 'regex',
    packages = find_packages('src'),
    package_dir={'': 'src'},
    install_requires = [
            'numpy==1.14.3',
            'pytest==3.6',
            ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite = 'tests'
)
