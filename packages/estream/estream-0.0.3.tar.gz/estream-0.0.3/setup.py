from setuptools import find_packages, setup

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="estream",
    version="0.0.3",
    author='Chanon Jenakom',
    author_email='chanonjenakom@gmail.com',
    description='An E-Stream implementation in Python',
    long_description=long_description,
    url='https://github.com/mickeycj/estream',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ],
    keywords='machine learning, data mining, stream clustering, evolution-based'
)
