import setuptools


with open('README.md') as f:
    long_description = f.read()


setuptools.setup(
    name='yapdfminer',
    use_scm_version=True,
    description='PDF parser and analyzer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/eladkehat/yapdfminer',
    author='Elad Kehat',
    author_email='eladkehat@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing',
    ],
    keywords=[
        'pdf',
        'pdf parser',
        'pdf converter',
        'layout analysis',
        'text mining',
    ],
    packages=setuptools.find_packages(exclude=['cmaprsrc', 'docs', 'samples', 'tests']),
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[
        'chardet ~= 3.0',
        'Pillow ~= 6.0',
        'pycryptodome ~= 3.8',
        'sortedcontainers ~= 2.1',
    ],
    setup_requires=['setuptools_scm'],
    scripts=[
        'tools/pdf2txt.py',
        'tools/dumppdf.py',
        'tools/latin2ascii.py',
    ]
)
