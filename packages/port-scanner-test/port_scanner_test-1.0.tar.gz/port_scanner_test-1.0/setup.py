from setuptools import setup

setup(
    name='port_scanner_test',
    version='1.0',
    description='port scanning tool',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='scanning port ip address',
      url='',
      author='',
      author_email='',
      license='Apache 2.0',
      packages=['port_scanner_test'],
      include_package_data=True,
      zip_safe=False
)


# python3 -m twine upload dist/*