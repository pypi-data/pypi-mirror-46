from setuptools import setup, find_packages

setup(name='imperituroard',
      version='0.4',
      description='Module for comunicate with staros device',
      long_description='Connection to staros device, like Cisco ASR5700 or Cisco ASR5000',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Text Processing :: Linguistic', ],
      keywords='monitoring additional procedures',
#      url='http://github.com/storborg/funniest',
      author='Dzmitry Buynovskiy',
      author_email='imperituro@mail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['paramiko', 'requests', 'subprocess.run'],
      include_package_data=True,
      zip_safe=False)
