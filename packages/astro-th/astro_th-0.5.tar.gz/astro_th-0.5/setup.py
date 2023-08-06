import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='astro_th',
    version='0.5',
    scripts=['init_read.py'],
    author='Taehwa Yoo',
    author_email='dbahck37@gmail.com',
    description="Taehwa Yoo's package",
    long_description=long_description

)
