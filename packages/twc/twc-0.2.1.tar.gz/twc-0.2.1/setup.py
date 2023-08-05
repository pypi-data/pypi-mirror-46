import sys

from setuptools import setup, find_packages


with open('README.rst', encoding='utf-8') as f_:
    long_description = f_.read()


def main():
    setup(name='twc',
          description="TaskWarrior's interactive terminal frontend",
          long_description=long_description,
          use_scm_version={'write_to': 'src/twc/_version.py'},
          license='GPLv3+',
          author='Michał Góral',
          author_email='dev@mgoral.org',
          url='https://gitlab.com/mgoral/twc',
          platforms=['linux'],
          setup_requires=['setuptools_scm'],
          install_requires=['prompt_toolkit==2.0.9',
                            'tasklib==1.1.0',
                            'attrs==19.1.0',
                            'mgcomm>=0.2.0'],

          # https://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=['Development Status :: 3 - Alpha',
                       'Environment :: Console',
                       'Intended Audience :: End Users/Desktop',
                       'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                       'Natural Language :: English',
                       'Operating System :: POSIX',
                       'Programming Language :: Python :: 3 :: Only',
                       'Programming Language :: Python :: 3.5',
                       'Programming Language :: Python :: 3.6',
                       'Programming Language :: Python :: 3.7',
                       'Topic :: Utilities',
                       ],

          packages=find_packages('src'),
          package_dir={'': 'src'},
          entry_points={
              'console_scripts': ['twc=twc.app:main'],
          },
          )


if __name__ == '__main__':
    main()
