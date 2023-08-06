import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()    

setuptools.setup(
    name='django-sysace',
    version='1.2.8',
    packages=setuptools.find_packages(),
    include_package_data=True,
    license='BSD License',  
    description='ACE is a Django app to administrate networks hosts, ip address, services, racks, patchpanels, phones and more. The system objective is turn the IT Infraestructure adminsitration easyer.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://www.rogeriodacosta.com.br/',
    author='Rogerio da Costa Dantas Luiz',
    author_email='rogeriocdluiz@gmail.com',
    install_requires=[
        'django-modalview==0.1.5',
        'django-autocomplete-light==3.2.9',
        'reportlab==2.5',
        'django-simple-history==1.9.0',
        'py2-ipaddress==3.4',
        'pisa==3.0.33',
        'html5lib==1.0b3',
        'Pillow==4.2.1',
        'django-import-export==0.4.5',
        'django-widget-tweaks==1.4.1',
        'django-mass-edit==2.7', 
        'django-filter==1.1.0',
        'django-widget-tweaks==1.4.1',
        'django-mail-templated==2.6.5',
        'django-solo==1.1.2',
        'django-extensions==2.1.5',
        'django-tables2==1.19.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],    
) 
