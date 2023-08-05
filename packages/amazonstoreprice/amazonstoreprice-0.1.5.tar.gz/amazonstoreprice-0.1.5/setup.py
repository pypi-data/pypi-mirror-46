import setuptools

setuptools.setup(
    name='amazonstoreprice',
    packages=['amazonstoreprice'],
    package_dir={'amazonestoreprice': 'amazonstoreprice'},
    version='0.1.5',
    install_requires=['requests', 'beautifulsoup4'],
    description='Find the price on Amazon store starting from url',
    author='Alessandro Sbarbati',
    author_email='miriodev@gmail.com',
    url='https://github.com/Mirio/amazonstoreprice',
    download_url='https://github.com/Mirio/amazonstoreprice/tarball/0.1',
    keywords=['Amazon', 'amazonprice', 'amazonstoreprice', "amazonstore"],
    license='BSD',
    classifiers=["License :: OSI Approved :: BSD License",
                 "Programming Language :: Python :: 3",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 "Topic :: Utilities"],
)
