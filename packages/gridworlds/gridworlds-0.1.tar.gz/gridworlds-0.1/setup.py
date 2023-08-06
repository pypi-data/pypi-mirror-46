from distutils.core import setup
setup(
  name = 'gridworlds',
  packages = ['gridworlds'],
  version = '0.1',
  license='MIT',
  description='Generate grids for AI bots',
  author = 'Ryan McCauley',
  author_email='ryanmccauley211@gmail.com',
  url = 'https://github.com/ryanmccauley211/gridworld',
  download_url = 'https://github.com/ryanmccauley211/gridworld/archive/0.1.tar.gz',
  keywords = ['artificial intelligence', 'grid', 'bot', 'generate', 'maze'],
  install_requires=[
          'pygame'
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
    'Programming Language :: Python :: 3.7'
  ],
)