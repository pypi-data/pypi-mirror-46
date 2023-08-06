from setuptools import setup, find_packages

with open("README.md", "r") as fh:
        long_description = fh.read()

setup(
    name='j2f',
    url='https://gitlab.com/jsenin/jinja-to-file.git',
    author='Jorge Senin',
    author_email='jorge@senin.org',
    maintainer_email='jorge@senin.org',
    version='0.0.3',
    description='Jinja 2 file command line render',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['Jinja2', 'PyYaml', 'cx_Freeze'],
    long_description=long_description,
    long_description_content_type="text/markdown",
)

