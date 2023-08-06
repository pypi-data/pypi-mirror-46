from setuptools import setup

setup(
    name='kapuccino',
    version='0.0.6',
    author='Enrique Coronado',
    author_email='enriquecoronadozu@gmail.mx',
    url='http://enriquecoronadozu.github.io',
    description='An Authoring Artificial Intelligence Modelling library',
    packages=["kapuccino"],
    install_requires=[
        'nep', 'transitions'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development"
    ]
)
