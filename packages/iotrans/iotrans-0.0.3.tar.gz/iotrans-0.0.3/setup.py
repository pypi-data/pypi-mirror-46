from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='iotrans',
    version='0.0.3',
    author='Open Data Toronto',
    author_email='opendata@toronto.ca',
    packages=['iotrans'],
    url='https://github.com/open-data-toronto/iotrans',
    license='MIT',
    description='A package to easily convert structured data into various file formats',
    long_description=long_description,
    install_requires=[
        'geopandas>=0.4.0',
        'xmltodict>=0.12.0'
    ],
    include_package_data=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
    keywords='',
)
