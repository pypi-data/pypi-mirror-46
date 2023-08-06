import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='cfl_data_utils',
    version='0.13.0',
    author='Will Garside',
    author_email='will@chetwood.co',
    description='Utilities for the Data and Analytics team at Chetwood Financial',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chetwoodfinancial/data-utilities',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['sshtunnel', 'pymysql', 'psycopg2-binary', 'requests', 'blessings', 'pandas', 'sqlalchemy']
)
