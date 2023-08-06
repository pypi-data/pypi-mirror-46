import setuptools

setuptools.setup(
    name='netrd',
    version='0.0.1',
    author='NetSI 2019 Collabathon Team',
    author_email='stefanmccabe@gmail.com',
    description='Repository of network reconstruction, distance, and simulation methods',
    url='https://github.com/netsiphd/netrd',
    packages=setuptools.find_packages(),
    classifiers=['Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent'],
    extras_require={
        'doc':  ['POT>=0.5.1'],
    }
)
