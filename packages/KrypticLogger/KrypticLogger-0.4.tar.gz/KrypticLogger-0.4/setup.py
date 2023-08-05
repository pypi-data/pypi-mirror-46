import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    #Here is the module name.
    name="KrypticLogger",
 
    #version of the module
    version="0.4",
 
    #Name of Author
    author="Kryptic Studio",
 
    #your Email address
    author_email="kennethc@kryptic-studio.com",
 
    #Small Description about module
    description="KrypticLogger is a tool to help better organize and minimizing the amount of code while logging! ",
 
    long_description=long_description,
 
    #Specifying that we are using markdown file for description
    long_description_content_type="text/markdown",
 
    #Any link to reach this module, if you have any webpage or github profile
    url="https://github.com/KrypticStudio/KrypticLogger/",
    packages=setuptools.find_packages(),
 
    #classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
