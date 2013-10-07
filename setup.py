from setuptools import setup

setup(name='langner',
      version='0.2',
      description='Langner - language for expressing behaviour strategies.',
      long_description='Object oriented language that combines event driven architecture and programing in logic.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Science/Research',
      ],
      keywords='langner strategies strategy logic',
      url='https://github.com/romankierzkowski/langner',
      author='Roman Kierzkowski',
      author_email='roman.kierzkowski@gmail.com',
      license='MIT',
      packages=['langner'],
      install_requires=[
          'ply',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=True)
