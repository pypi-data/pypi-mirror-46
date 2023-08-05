from setuptools import setup, find_packages
setup(
    name='TalesParse',
    version='1.0.0',
    description='Scraping good and bad tales.',
    py_modules=["TalesParse"],
    packages=["TalesParse"],
    install_requires=["bs4", "requests"],
    istall_package_data=True,

    entry_points={
        'console_scripts':
            ['TalesParse = TalesParse.Scraper']
        }
            
)