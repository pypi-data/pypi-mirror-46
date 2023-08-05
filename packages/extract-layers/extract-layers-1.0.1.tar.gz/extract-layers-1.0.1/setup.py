from setuptools import setup

setup(
    name="extract-layers",
    version="1.0.1",
    py_modules=["extract_layers"],
    install_requires=[
        "Click",
        "xmltodict"
    ],
    entry_points="""
        [console_scripts]
        extract-layers=extract_layers:interface
    """,
)
