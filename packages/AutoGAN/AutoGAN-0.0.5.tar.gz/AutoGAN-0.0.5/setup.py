from setuptools import setup, find_packages

setup(name='AutoGAN',
      version='0.0.5',
      description='GANs were never easier',
	  classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
		'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
		],
      keywords='keras gan gans ai',
      url='http://github.com/EladDv/AutoGAN_Test',
      author='Elad Dvash',
      license='MIT',
      packages=find_packages(),
	  install_requires=[
		'tensorflow<=1.13',
		'keras>=2'
      ])
