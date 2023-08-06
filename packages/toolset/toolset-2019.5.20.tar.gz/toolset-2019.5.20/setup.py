import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='toolset',
    version='2019.5.20',
    author='Czw',
    author_email='459749926@qq.com',
    description='Tool set.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Czw96/ToolSet',
    packages=setuptools.find_packages(exclude=('trash',)),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['cryptography'],
)
