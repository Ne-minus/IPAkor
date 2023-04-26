import setuptools

setuptools.setup(name='IPAkor',
                 version='2.2',
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 classifiers=[
                     'Programming Language :: Python :: 3',
                     'Operating System :: OS Independent',
                     'Topic :: Scientific/Engineering'
                 ],
                 install_requires=['konlpy', 'wget'],
                 python_requires='>=3',
                 author_email='neminova2.0@gmail.com'
                 )