from setuptools import setup

# Used in pypi.org as the README description of your package
with open("README.md", 'r') as f:
    long_description = f.read()

setup(
        name='altoshift', 
        version='0.1.20',
        description='learning today make you better tomorrow',
        author='eko',
        author_email='eko@altoshift.com',
        license="MIT",
        url="https://altoshift.com",
        packages=['altoshift'],
        #scripts=['scripts/some_script.py'],
        #python_requires='>=3',
        requires=['requests(>=1.2.3)','pandas','xlrd'],
        install_requires=[
            'pandas',
            'xlrd',
            'requests'
        ],
        long_description=long_description
)