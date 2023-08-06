from setuptools import setup, find_packages

setup(
    name="Terrene",
    version="2.0.4",
    description="Terrene's Python SDK",
    url="https://docs.terrene.co",
    author="Terrene",
    author_email="developers@terrene.co",
    license='MIT',
    keywords="terrene",
    packages=find_packages(),
    install_requires=['requests', 'pandas', 'numpy'],
    test_requirements=[],
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
