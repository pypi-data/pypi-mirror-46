from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='logomaker',
      version='0.7',
      description='Package for making Sequence Logos',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='Sequence Logos',
      url='http://logomaker.readthedocs.io',
      author='Ammar Tareen, Justin B. Kinney',
      author_email='tareen@cshl.edu',
      license='MIT',
      packages=['logomaker'],
#      package_data={'logomaker': ['src/*']},
      include_package_data=True,
      install_requires=[
        'numpy',
		'matplotlib',
		'pandas',
		'glob2',
		'glob3'
      ],
      zip_safe=False)