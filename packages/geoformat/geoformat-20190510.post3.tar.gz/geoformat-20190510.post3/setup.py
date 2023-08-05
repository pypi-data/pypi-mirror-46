from setuptools import setup


markdown_path = 'README.md'
# try:
#     import pypandoc
#     read_me_rst = pypandoc.convert(markdown_path, 'rst')
# except:
with open(markdown_path, encoding='utf-8') as read_me_file:
    read_me_rst = read_me_file.read()



setup(
    name='geoformat',
    version='20190510.post3',
    url='https://framagit.org/Guilhain/Geoformat',
    license='MIT',
    author='Guilhain Averlant',
    author_email='g.averlant@mailfence.com',
    description='Geoformat is a GDAL/OGR library overlayer',
    long_description=read_me_rst,
    long_description_content_type='text/markdown',
    py_modules=['geoformat'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: GIS",
    ]
)
