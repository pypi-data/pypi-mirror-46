from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="py-cobra",
    version='0.0.0.dev1',
    description='Cobra Framework',
    long_description=long_description,
    license='MIT',
    author='Meheret Tesfaye',
    author_email='meherett@zoho.com',
    url='https://github.com/meherett/py-cobra',
    python_requires='>=3.6,<3.8',
    packages=['cobra'],
    install_requires=[
    ],
    entry_points={
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
