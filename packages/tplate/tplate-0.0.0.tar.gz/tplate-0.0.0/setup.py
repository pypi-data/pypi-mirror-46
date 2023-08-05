import setuptools

setuptools.setup(
    name='tplate',
    author='Randy May',
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts' : ['tplate=tplate.commandline:run']
    },
    license='MIT',
    install_requires=['PyYaml','Jinja2']
)
