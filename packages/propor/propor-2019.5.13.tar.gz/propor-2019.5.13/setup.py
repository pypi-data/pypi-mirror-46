import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='propor',
    version='2019.5.13',
    author='Czw_96',
    author_email='459749926@qq.com',
    description='Project porter.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Czw96/propor',
    packages=setuptools.find_packages(exclude=('trash',)),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': ['propor-get=propor.get:_get', 'propor-put=propor.put:_put'],
    },
    install_requires=[
        'paramiko',
    ],
)
