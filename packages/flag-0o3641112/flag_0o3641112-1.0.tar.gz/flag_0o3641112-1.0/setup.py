from setuptools import setup, find_packages

README = ''

setup_args = dict(
    name='flag_0o3641112',
    version='1.0',
    description='desc',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='OsOmE1',
    author_email='',
    keywords=['simple_codecs', 'Encryption', 'Encoding'],
    url='',
    download_url='https://pypi.org/project/flag_0o3641112/'
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)