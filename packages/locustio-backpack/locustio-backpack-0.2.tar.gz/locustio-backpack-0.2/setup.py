import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='locustio-backpack',  
     version='0.2',
     author="Alin-Marian Iuga",
     author_email="alin.m.iga@gmail.com",
     description="Locust Framework Extension",
     long_description=long_description,
    long_description_content_type="text/markdown",

     packages=setuptools.find_packages(),
     classifiers=[
         "Development Status :: 3 - Alpha"
        #  "Intended Audience :: Developers",
        #  "License :: MIT License",
        #  "Operating System :: OS Independent",
     ],
     python_requires='>=2.7',
     install_requires=['pandas==0.23.4',
                        'setuptools==41.0.1',
                        'wget==3.2',
                        'numpy==1.15.4',
                        'gevent==1.3.7',
                        'matplotlib==2.2.4',
                        'requests==2.21.0',
                        'locustio==0.9.0'
                        ]
 )