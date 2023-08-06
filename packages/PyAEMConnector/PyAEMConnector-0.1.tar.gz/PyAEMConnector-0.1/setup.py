from distutils.core import setup
setup(
  name = 'PyAEMConnector',        
  packages = ['PyAEMConnector'],  
  version = '0.1',      
  license='MIT', 
  description = 'Python library for connecting to Adobe Experience Manager (AEM)',   
  author = 'Ashokkumar T.A',                  
  author_email = 'ashokkumar.ta@gmail.com',   
  url = 'https://github.com/ashokkumarta',   
  download_url = 'https://github.com/ashokkumarta/PyAEMConnector/archive/v_01.tar.gz', 
  keywords = ['AEM', 'Connector', 'Python AEM Utility'],   
  install_requires=[  
      'requests',          
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)

