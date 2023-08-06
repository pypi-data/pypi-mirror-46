from setuptools import setup

setup(
    name="metabot2txt",
    version="0.0.1",
    description="convert images of well structured tables to text",
    url="https://github.com/HeitorBoschirolli/metabot2txt",
    author="Heitor Boschirolli",
    author_email="heitor.boschirolli@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["metabot2txt"],
    include_package_data=True,
    install_requires=["pillow", "pytesseract", "scikit-image"],
    entry_points={
        "console_scripts": [
            "metabot2txt=metabot2txt.__main__:main"
        ]
    }
)
