from setuptools import setup

setup(name='speculationcc',
      version='0.1.1',
      description='sentiment analysis for speculationcc',
      url='http://github.com/wilkosz/crypto-profiler',
      author='joshua wilkosz',
      author_email='joshua@wilkosz.com.au',
      license='MIT',
      packages=['speculationcc'],
      scripts=['bin/speculationcc-cmd'],
      install_requires=[
        'nltk'
      ],
      dependency_links=[],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
