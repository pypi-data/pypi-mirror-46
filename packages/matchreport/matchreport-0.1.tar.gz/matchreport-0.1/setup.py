from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='matchreport',
      version='0.1',
      description='Creates analysis reports for GAA matches',
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Natural Language :: English',
            'Topic :: Text Processing :: Linguistic',
      ],
      url='https://github.com/moynihanrory/matchreport',
      author='Rory Moynihan',
      author_email='ruaraidho@gmail.com',
      license='MIT',
      packages=['matchreport'],
      install_requires=[
            'pandas',
            'xmltodict',
            ],
      zip_safe=False,
      test_suite='matchreport',
      tests_require=['matchreport'],
      entry_points={
            'console_scripts': ['matchreport=matchreporter.matchreport:main'],
      })