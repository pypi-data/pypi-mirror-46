from setuptools import setup, find_packages

pkj_name = 'esputnik'

with open('requirements.txt') as f:
    requires = f.read().splitlines()


setup(
    name='ok-esputnik',
    version='0.2',
    description='Simple E-Sputnik REST client library for Python.',
    long_description=open('README.rst').read(),
    author='Oleg Kleschunov',
    author_email='igorkleschunov@gmail.com',
    url='https://github.com/LowerDeez/ok-esputnik',
    packages=[pkj_name] + [pkj_name + '.' + x for x in find_packages(pkj_name)],
    include_package_data=True,
    license='MIT',
    install_requires=requires,
    python_requires=">=3.5",
    classifiers=[
        'Environment :: Web Environment',
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]

)
