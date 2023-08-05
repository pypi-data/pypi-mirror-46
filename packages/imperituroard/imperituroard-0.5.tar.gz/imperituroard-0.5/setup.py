from setuptools import setup, find_packages

setup(name='imperituroard',
      version='0.5',
      description='Procedures from imperituroard',
      long_description='Different usefull procedures from imperituroard',
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
