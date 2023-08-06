import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nodifly",
    version="1.1.3",
    author="Stephen Hsu",
    author_email="nodiflycontact@gmail.com",
    description="Nodifly - Real Time Notifications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stephenjhsu/nodifly",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
          'console_scripts': [
              'nodifly = nodifly.__main__:main'
          ]
      },
    #"name_of_executable = module.with:function_to_execute"
)