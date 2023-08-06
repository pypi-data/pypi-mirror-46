#! /usr/bin/env python


from setuptools import setup
setup(
    name='mdx-footnotes2',
    version='0.2.0',
    author='Manfred Stienstra, Yuri takhteyev and Waylan limberg',
    author_email='waylan.limberg@icloud.com',
    description='The official Python markdown "footnotes" extension, with additional options.',
    url='https://github.com/wilhelmer/mdx-footnotes2',
    py_modules=['footnotes2'],
    install_requires=['Markdown>=2.0',],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
