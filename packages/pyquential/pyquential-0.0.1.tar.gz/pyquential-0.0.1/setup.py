from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pyquential',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    version='0.0.1',
    description='Extension functions for iterables to ease functional programming.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Kevin Winter',
    author_email='kevin.n.winter@gmail.com',
    license='MIT',
    install_requires=[
        'numpy',
        'pandas',
        'pylantern',
        'pyfunctional',
        'forbiddenfruit'
    ]
)