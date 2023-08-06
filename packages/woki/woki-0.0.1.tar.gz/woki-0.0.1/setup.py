import setuptools




setuptools.setup(
    name="woki",
    version="0.0.1",
    author="Ujala Jha",
    author_email="jhaujala43@gmail.com",
    description="A small package to search wikipedia",
    long_description="A tool to search wikipedia",
    long_description_content_type="text/markdown",
    url="https://github.com/ujalajha43/woki",
    packages=setuptools.find_packages(),
    install_requires=[
          'wikipedia'
      ],
      zip_safe=False,
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
