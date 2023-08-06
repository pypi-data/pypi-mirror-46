from setuptools import setup
import io
import os

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


NAME = 'opengen'
VERSION = '0.0.4'

setup(name=NAME,
      version=VERSION,
      description='Optimization Engine Code Generator',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=['Pantelis Sopasakis', 'Emil Fresk'],
      author_email='p.sopasakis@gmail.com',
      license='MIT License',
      packages=['opengen', 'opengen.builder', 'opengen.config', 'opengen.functions'],
      include_package_data=True,
      install_requires=[
          'jinja2', 'casadi', 'numpy'
      ],
      classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: MIT License',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Rust',
            'Intended Audience :: Science/Research',
            'Topic :: Software Development :: Libraries',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Topic :: Software Development :: Code Generators',
            'Topic :: Software Development :: Embedded Systems'
      ],
      keywords = ['optimization', 'nonconvex', 'embedded'],
      url=(
            'https://github.com/alphaville/optimization-engine'
      ))
