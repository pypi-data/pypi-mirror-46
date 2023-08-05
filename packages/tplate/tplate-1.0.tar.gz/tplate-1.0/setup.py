import setuptools

setuptools.setup(
    name='tplate',
    version='1.0',
    author='Randy May',
    description='A project templating tool that based on Jina2',
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts' : ['tplate=tplate.commandline:run']
    },
    license='MIT',
    install_requires=['PyYaml>=5.1','Jinja2>=2.10.1']
)
