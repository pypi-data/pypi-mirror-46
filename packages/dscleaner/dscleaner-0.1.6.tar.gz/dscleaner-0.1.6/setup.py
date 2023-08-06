import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dscleaner',
    version='0.1.6',
    author='Manuel Pereira',
    author_email='afonso.pereira4525@gmail.com',
    packages=['dscleaner',],
    url='http://pypi.python.org/pypi/dscleaner/',
    license='The MIT License',
    description='Useful energy dataset tools to fix length, inconsistencies and convertion to a sound file format',
    long_description=long_description,
    install_requires=[
        "PySoundFile >= 0.9.0.post1",
        "librosa >= 0.6.3",
        "numpy >= 1.16.1",
        "pandas >= 0.24.1",
    ],
)