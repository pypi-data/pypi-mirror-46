import setuptools

with open('README.md') as f:
    long_description = f.read()
setuptools.setup(
    name = 'lazyplotly',
    version = '1.1',
    author = 'chuboy',
    description = 'A wrapper of plolty which makes adding widget much more easy (and lazy)',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/billju/lazyplotly',
    packages = setuptools.find_packages(),
    classifiers = [
        "Topic :: Scientific/Engineering :: Visualization",
    ]
)
#python setup.py sdist bdist_wheel
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#twine upload dist/*