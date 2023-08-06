import setuptools

setuptools.setup(
        name="cloud-logger",
        version="0.1.1",
        author="furodrive",
        author_email="furodrive@gmail.com",
        packages=setuptools.find_packages(),
        install_requires=[
          'boto3',
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License"
        ]
)
