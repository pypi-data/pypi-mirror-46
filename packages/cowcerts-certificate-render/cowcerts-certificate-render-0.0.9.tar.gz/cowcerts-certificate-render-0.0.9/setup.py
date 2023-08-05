"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path, walk
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# Data files
# https://stackoverflow.com/a/36693250
def package_files(directory):
    paths = []
    for (current_path, directories, filenames) in walk(directory):
        for filename in filenames:
            paths.append(path.join('..', current_path, filename))
    return paths

# Pipenv dependencies
def find_pipenv_dependencies():
    import pipfile
    return list(map(lambda x: x, pipfile.load().data['default']))


setup(
    name='cowcerts-certificate-render',
    version='0.0.9',
    description='HTML template render for Cowcerts certificates visualization',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/btcalabs/certificate-render',
    author='BTCA Labs',
    author_email='btcalabs+cowcerts+certificate-render@btcassessors.com',
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='cowcerts certificate template html render',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=["jinja2", "beautifulsoup4", "htmlmin", "inlinestyler", "flask", "livereload"],
    # extras_require={  # Optional
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
    package_data={
        'cowcerts_certificate_render': package_files(
            path.join("cowcerts_certificate_render", "data")),
    },
    entry_points={
        'console_scripts': [
            'cowcerts-certificate-render=cowcerts_certificate_render.__main__:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://gitlab.com/btcalabs/certificate-render/issues',
        'Source': 'https://gitlab.com/btcalabs/certificate-render',
    },
)
