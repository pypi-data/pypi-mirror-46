import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(name='xltojson',
      version='1.1.0',
      description='This python package translates Excel data to JSON',
      author='Vishal Pant',
      author_email='vishalpant.pant65@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/vishalpant/xltojson",
      packages=setuptools.find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      install_requires=[
          'xlrd==1.2.0',
          'pandas==0.24.2',
      ],
      zip_safe=False,
      python_requires='==3.6')




