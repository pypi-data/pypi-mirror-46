import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name='pysetup',
    version='2019.5.13',
    author='Czw_96',
    author_email='459749926@qq.com',
    description='Pypi upload tool.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Czw96/PySetup',
    packages=setuptools.find_packages(exclude=('trash',)),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'setuptools',
        'wheel',
        'twine',
    ],
    entry_points={
        'console_scripts': ['pysetup=pysetup.main:main'],
    },
)
