from distutils.core import setup
setup(
  name = 'image_layer_decomposition',
  packages = ['image_layer_decomposition'],
  version = '0.3',
  license='MIT', 
  description = 'Color image layer decomposition',
  author = 'Karolina Tretyakova',
  author_email = 'tretyakovakarolina@gmail.com',
  url = 'https://github.com/katretyakova', 
  download_url = 'https://github.com/katretyakova/image-layer-decomposition/archive/v_03.tar.gz',
  keywords = ['image', 'decomposition'],
  install_requires=[
          'numpy',
          'scipy',
          'Pillow',
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