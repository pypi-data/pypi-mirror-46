from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='simple_codecs',
    version='1.0',
    description='Useful tools to with encoding and encryption',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='OsOmE1',
    author_email='',
    keywords=['ced', 'Encryption', 'Encoding'],
    url='https://github.com/OsOmE1/ced',
    download_url='https://pypi.org/project/simple_codecs/'
)

install_requires = [
    'simple_codecs',
    'PyCrypto',
    'Crypto'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)