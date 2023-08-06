from setuptools import setup

requirements = [
      'pysam',
      'pandas',
      'pybedtools',
      'sklearn',
      'matplotlib'


]

setup(name="py-popgen",
      version="0.0.1",
      description="first setup file",
      include_package_data=True,
      packages=['pgpipe'],
      #install_requires=requirements,
      scripts=['pgpipe/vcf_phase.py'])

#packages=setuptools.find_packages() to automate package finding?
