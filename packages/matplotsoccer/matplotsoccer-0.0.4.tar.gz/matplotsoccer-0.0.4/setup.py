import setuptools

setuptools.setup(name='matplotsoccer',
      version='0.0.4',
      description='Library for visualizing soccer event stream data',
      url='http://github.com/tomdecroos/matplotsoccer',
      author='Tom Decroos',
      author_email='tom.decroos.be@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(exclude=["notebooks"]),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
     ],
      )