import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
  name = 'towise',         # How you named your package folder (MyLib)
  packages = setuptools.find_packages(),   # Chose the same as "name"
  version = '0.1.7',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Towise assists you to detect human faces and bodies with using the latest and reliable technology.',   # Give a short description about your library
  author='Harun KELEŞOĞLU',
  author_email='harunkelesoglu_@hotmail.com',
  url = 'https://github.com/argedor/TowisePythonAPI.git',   # Provide either the link to your github or to your website
  download_url = "https://github.com/argedor/TowisePythonAPI/archive/1.7.tar.gz",    # I explain this later on
  keywords = ['towise', 'face detection', 'body detection','emotion detection','face comparing'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
           'requests'
      ],
  classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
  ],
)