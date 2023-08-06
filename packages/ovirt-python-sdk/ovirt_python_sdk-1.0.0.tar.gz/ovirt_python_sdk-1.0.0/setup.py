import setuptools

setuptools.setup(
    name='ovirt_python_sdk',
    version='1.0.0',
    author='Toliak, Underlor',
    author_email='cfyz_74@mail.ru',
    url='https://github.com/gamehost/ovirt_python_sdk',
    description='Ovirt Python SDK',
    install_requires=[
        'ovirt-engine-sdk-python',
    ],
    packages=setuptools.find_packages(),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description='GIT: https://github.com/gamehost/ovirt_python_sdk',
)