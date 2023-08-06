from setuptools import setup, find_packages

setup(
    name="rv-schubert-sdk",
    author="Raphael Schubert",
    author_email="rfswdp@gmail.com",
    description="SDK de integracao com RV Tecnologia",
    url="https://github.com/rfschubert/rv-schubert-sdk",
    version='1.1.0',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'xmltodict',
        'requests',
        'pendulum',
    ],
    include_package_data=True,
)
