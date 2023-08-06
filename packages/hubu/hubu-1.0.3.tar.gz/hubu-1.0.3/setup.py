from setuptools import setup, find_packages
from hubu import __version__


def requirements():
    with open('requirements.txt') as f:
        return [dep for dep in f.read().split('\n')
                if dep.strip() != '' and not dep.startswith('-e')]


with open("README.md", "r") as f:
    long_description = f.read()

setup(name='hubu',
      version=__version__,
      packages=find_packages(),
      url='https://github.com/yitsushi/hubu',
      author='Balazs Nadasdi',
      author_email='balazs.nadasdi@cheppers.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=True,
      include_package_data=True,
      install_requires=requirements(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Operating System :: OS Independent",
      ],
      entry_points="""
      [console_scripts]
      hubu = hubu.main:main
      """)

