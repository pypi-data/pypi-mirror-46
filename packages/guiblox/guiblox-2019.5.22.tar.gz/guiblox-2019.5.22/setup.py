### Reference: https://github.com/Terrabits/rohdeschwarz/blob/master/setup.py
### Reference: https://python-packaging.readthedocs.io/en/latest/minimal.html
### 
### python setup.py register #Reserve name in pypi
### python setup.py --help-commands
### python setup.py bdist    #Creates <pkg>.zip
### python setup.py install  #Installs package
### python setup.py install_scripts
### pip install .            #Installs package in directory
### pip install -e .         #Install editable package
##########################################################
### Upload to PyPi
### python setup.py sdist    #Creates <pkg>.tar.gz
### twine upload .\dist\rssd-0.1.8.tar.gz 

import os
from datetime   import datetime
from setuptools import setup, find_packages
dateVer = datetime.now().strftime("%Y.%m.%d")

with open('README.md') as f:
    long_description = f.read()

setup(name='guiblox',
    version=dateVer,
    description='GUI Widgets in Frames',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    classifiers=[
      'Development Status :: 3 - Alpha',      #3:Alpha 4:Beta 5:Production/Stable
      'License :: Other/Proprietary License',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3.7',
      'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
    ],
    keywords='tkinter',
    url='https://github.com/mclim9/guiblox',
    author='Martin C Lim',
    author_email='martin.lim@rsa.rohde-schwarz.com',
    license='R&S Terms and Conditions for Royalty-Free Products',
    packages=find_packages(exclude=['test','proto']),
    install_requires=[      ],
    test_suite = 'test',
    include_package_data=True,
    zip_safe=False)

# if __name__ == "__main__":
#    os.system("python setup.py sdist")