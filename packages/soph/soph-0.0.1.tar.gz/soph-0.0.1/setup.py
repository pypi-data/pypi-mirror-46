from setuptools import setup, find_packages

setup(
    name='soph',
    version='0.0.1',
    url='https://github.com/artificialsoph/soph.py',
    author='soph',
    author_email='s@soph.info',
    packages=find_packages(),
    install_requires=[
        "keras",
        "numpy",
        "tensorflow",
        "seaborn",
        "matplotlib",
        "sklearn",
    ],
    include_package_data=True,
)
