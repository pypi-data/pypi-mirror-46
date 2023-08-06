from setuptools import setup

setup(name='secure_project',
      version='0.1',
      description='demonstration for class',
      py_modules=['wordcount_lib'],
      scripts=['wordcount'],
      setup_requires=[
          'pytest-runner',
      ],
      tests_require=[
          'pytest',
      ],
)      
