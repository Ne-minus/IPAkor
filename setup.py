import setuptools

setuptools.setup(name='IPAkor',
                 version='2.4',
                 package_data={'static': ['*']},
                 packages=setuptools.find_packages(),
                 classifiers=[
                     'Programming Language :: Python :: 3',
                     'Operating System :: OS Independent',
                     'Topic :: Scientific/Engineering'
                 ],
                 install_requires=['konlpy', 'wget'],
                 python_requires='>=3',
                 author_email='neminova2.0@gmail.com'
                 )
