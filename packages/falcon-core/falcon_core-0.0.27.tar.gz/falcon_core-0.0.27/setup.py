from setuptools import setup, find_packages


def read(file):
    with open(file) as f:
        return f.read()


setup(
    name='falcon_core',
    version='0.0.27',
    description='Falcon Core Inspired by Django for Falcon API Framework.',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Maksym Sichkaruk',
    author_email='maxim.18.08.1997@gmail.com',
    license='MIT',
    url='https://github.com/Maksych/falcon_core',
    packages=find_packages(
        include=['falcon_core.*', 'falcon_core'],
        exclude=['tests.*', 'tests'],
    ),
    include_package_data=True,
    scripts=['falcon_core/bin/falcon-core.py'],
    entry_points={'console_scripts': [
        'falcon-core = falcon_core.management:execute_from_command_line',
    ]},
    zip_safe=False,
    install_requires=['falcon', 'waitress', 'gunicorn'],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
