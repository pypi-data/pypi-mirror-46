from setuptools import setup, find_packages

setup(
    name='spiderbro',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    url='https://gitlab.com/granitosaurus/spiderbro',
    license='GPLv3',
    author='Bernardas Ališauskas',
    author_email='bernardas.alisauskas@pm.me',
    description='tools and scripts for web scraping',
    install_requires=[
        'requests',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'sb-join-csvs=spiderbro.data.join_csvs:main',
        ]
    },

)
