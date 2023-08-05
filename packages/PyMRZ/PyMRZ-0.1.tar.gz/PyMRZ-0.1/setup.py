from distutils.core import setup
setup(
  name = 'PyMRZ',         
  packages = ['pymrz'],
  version = '0.1',     
  license='MIT',      
  description = 'Generate and Read Machine Readable Zones (MRZs) with Python',   
  author = 'Aron Buzinkay',                  
  url = 'https://github.com/MrArobuz/pymrz', 
  download_url = 'https://github.com/MrArobuz/pymrz/archive/v0.1.tar.gz',
  keywords = ['mrz', 'passport', 'read mrz'],  
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
