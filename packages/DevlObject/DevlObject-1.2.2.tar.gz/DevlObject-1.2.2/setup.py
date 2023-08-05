from distutils.core import setup

setup(
  name = 'DevlObject',
  packages = ['DevlObject'],
  version = '1.2.2',
  license='MIT',
  description = 'Convert A Object To Json',
  author = 'YOUR NAME',
  author_email = 'your.email@domain.com',
  url = 'https://github.com/user/reponame',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords = ['DevlObject'],
  install_requires=[
          'beautifulsoup4',
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
  ],
)