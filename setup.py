from setuptools import setup

setup(
    name="json_to_model",
    version="1.0.4",
    license='MIT',
    description="automatically convert json to model defination",
    author='clowwindy',
    author_email='clowwindy42@gmail.com',
    url='https://github.com/clowwindy/json_to_model',
    packages=['json_to_model', 'json_to_model.generators'],
    package_data={
        'json_to_model': ['README.rst', 'LICENSE'],
        'json_to_model.generators': ['templates/*']
    },
    install_requires=[
                      'Inflector==2.0.1',
                      'Jinja2',
    ],
    entry_points="""
    [console_scripts]
    json_to_model = json_to_model.console:main
    """,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
