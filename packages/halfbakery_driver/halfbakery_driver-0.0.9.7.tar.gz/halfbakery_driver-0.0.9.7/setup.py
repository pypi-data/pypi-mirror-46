from setuptools import find_packages, setup

setup(
    name='halfbakery_driver',
    version='0.0.9.7',
    description='Halfbakery Communal Database controller.',
    url='https://github.com/drivernet/halfbakery_driver',
    author='Mindey',
    author_email='mindey@qq.com',
    license='PUBLIC BENEFIT',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=['metadrive'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False
)
