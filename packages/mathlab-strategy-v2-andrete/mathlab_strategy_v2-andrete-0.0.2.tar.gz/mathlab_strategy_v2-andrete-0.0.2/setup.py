import setuptools

with open("README.md", "r") as fh:
        long_description = fh.read()

        setuptools.setup(
            name="mathlab_strategy_v2-andrete",
            version="0.0.2",
            author="andrete",
            author_email="13120309879@163.com",
            description="mathlab strategy framework",
            long_description=long_description,
            long_description_content_type="text/markdown",
            url="https://github.com/mathlabchina/Pythagoras",
            packages=setuptools.find_packages(),
            classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],
            install_requires=[
                'pandas',
                'TA-Lib',
                'requests'
            ]

        )
