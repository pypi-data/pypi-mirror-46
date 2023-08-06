from distutils.core import setup
setup(
  name = 'ruengdech',         # How you named your package folder (MyLib)
  packages = ['ruengdech'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Test my First library to present my Information',   # Give a short description about your library
  author = 'RUENGDECH',                   # Type in your name
  author_email = 'ruengdech@gmail.com',      # Type in your E-Mail
  #do crate git-hub representary
  url = 'https://github.com/ruengdech/introduce_myself',   # Provide either the link to your github or to your website 
  download_url = 'https://github.com/ruengdech/introduce_myself/archive/v0.2.tar.gz',    # I explain this later on
  #Create in release 
  keywords = ['RUENGDECH', 'FIRST_PHTHON', 'HELLO WORLD'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second # this is include in my package
          'requests',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
'''
UPPER iS SET UP TEMPLATE
'''