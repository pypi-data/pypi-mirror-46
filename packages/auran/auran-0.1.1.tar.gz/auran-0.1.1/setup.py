from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='auran',
      version='0.1.1',
      description='auran is a python package built on top of pytorch to ease creation of artificial neural networks.',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.0',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
      keywords='',
      url='',
      author='Francois Lagunas',
      author_email='francois.lagunas@m4x.org',
      license='MIT',
      packages=['auran', 'auran.ann'],
      install_requires=['click'],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['auran_run=auran.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
