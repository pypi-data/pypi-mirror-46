from setuptools import setup 
  
 
# specify requirements of your package here 
REQUIREMENTS = [''] 
  
# some more details 
CLASSIFIERS = [ 
    'Development Status :: 4 - Beta', 
    'Intended Audience :: Developers', 
    'Topic :: Internet', 
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python', 
    'Programming Language :: Python :: 3.6', 
    ] 
  
# calling the setup function  
setup(name='writeLog', 
      version='0.0.4', 
      description='A log writer function for py based docker containers.', 
      long_description='',
      url='', 
      author='Jacob Stewart', 
      author_email='jick.68.0@gmail.com', 
      license='MIT', 
      packages=[''], 
      classifiers=CLASSIFIERS, 
      install_requires=REQUIREMENTS, 
      keywords='logger'
      ) 

