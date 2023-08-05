import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'PyLumiGateway',
    install_requires=['cryptography>=2.1.1'],
    version = '0.12.3',
    description = 'A library to communicate with the Lumi Gateway',
    author='Serkan Yilmaz',
    author_email="onlytango@gmail.com",
    url='https://github.com/Danielhiversen/PyXiaomiGateway/',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
)

