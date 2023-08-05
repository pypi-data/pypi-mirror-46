from setuptools import setup, find_packages

setup(
   name='kneejerk',
   version='1.0.1',
   description='A package for labelling image data with your quick, kneejerk reactions.',
   author='NapsterInBlue',
   author_email='NapsterInBlue@google.com',
   license='MIT',
   url='https://github.com/NapsterInBlue',
   packages=find_packages(include=['kneejerk', 'kneejerk.*']),  #same as name
   install_requires=['opencv-python',
                     'Click',
                     'matplotlib',
                     'numpy'], #external packages as dependencies

   entry_points={
    'console_scripts': [
        'kneejerk = kneejerk.cli:main',
        ],
    }
)
