from setuptools import setup

setup(
    name='swiftdownload',
    version='1.0.8',
    author="Sunil Muliki",
    author_email="Sunil.Muliki0@walmart.com",
    description="Python script which helps to download objects from object store using click",
    url="https://gecgithub01.walmart.com/s0m03fe/swift-click-download",
    py_modules=['swiftdownload'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Click',
        'python-swiftclient',
    ],
    entry_points='''
        [console_scripts]
        swiftdownload=swiftdownload:download_script
    ''',
)
