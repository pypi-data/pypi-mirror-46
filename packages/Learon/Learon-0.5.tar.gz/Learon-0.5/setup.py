from setuptools import setup

setup(name='Learon',
      version='0.5',
      description='High Level Machine Learning',
      author='Daron Théo',
      author_email='eclairbleu12@gmail.com',
      license='MIT',
      packages=['learon'],
      install_requires=[
          'scikit-learn',
      ],
      zip_safe=False)
