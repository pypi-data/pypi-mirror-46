import setuptools
import os

root_dir = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(root_dir, 'readme.rst')).read()

setuptools.setup(
    name="SmoothNLP",
    version="0.2.5",
    author="Ruinan(Victor) Zhang, Jun Yin",
    author_email="ruinan.zhang@icloud.com, yjun1989@gmail.com",
    description="Python Package for SmoothNLP Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhangruinan/SmoothNLP",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        "jpype1>=0.6.2",
        "requests"
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)