from setuptools import setup, find_packages

setup(
    name='hufflepuff',
    version='1.4',

    author='Peter Ward',
    author_email='peteraward@gmail.com',
    description='Hufflepuffs are particularly good finders.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://hg.flowblok.id.au/hufflepuff',

    packages=find_packages(),

    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=['six'],

    entry_points={
        'console_scripts': [
            'hufflepuff = hufflepuff.cli:main',
        ]
    },
)
