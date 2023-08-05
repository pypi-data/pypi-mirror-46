from setuptools import setup

with open('README.rst') as read_me_file:
    read_me_txt = read_me_file.read()

setup(
    name='geoformat',
    version='20190509.post2',
    url='https://framagit.org/Guilhain/Geoformat',
    license='MIT',
    author='Guilhain Averlant',
    author_email='g.averlant@mailfence.com',
    description='Geoformat is a GDAL/OGR library overlayer',
    long_description=read_me_txt,
    py_modules=['geoformat']
)
