from setuptools import find_packages, setup

import versioneer

setup(name='ngeo',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Fast and accurate spatial analysis',
      url='http://github.com/parietal-io/ngeo',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True)
