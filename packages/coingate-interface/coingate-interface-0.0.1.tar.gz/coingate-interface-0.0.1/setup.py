import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='coingate-interface',
    version='0.0.1',
    author='fly1ngDream',
    author_email='fly1ngDream@protonmail.com',
    description='Coingate API for humans',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
