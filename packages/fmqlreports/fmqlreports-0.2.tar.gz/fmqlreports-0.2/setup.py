from setuptools import setup

setup(name='fmqlreports',
      description = 'FMQL Reports',
      long_description = """A Python framework and set of executables for generating specific reports on VistA data cached using FMQL.""",
      version='0.2',
      install_requires = [
          'fmqlutils>=2.4.4',
          'numpy>=1.16.3'
      ],
      classifiers = ["Development Status :: 4 - Beta", "Programming Language :: Python :: 2.7"],
      url='http://github.com/Caregraf/FMQL/fmqlreports',
      license='Apache License, Version 2.0',
      keywords='VistA,FileMan,CHCS,FMQL,Caregraf',
      # install_requires=["pytz"], - problem OSX 
      package_dir = {'fmqlreports': ''},
      packages = ['fmqlreports', 'fmqlreports.basics', 'fmqlreports.patient'],
      entry_points = {
      }
)
