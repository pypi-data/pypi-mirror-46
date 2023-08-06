import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hs_rpc",
    version="0.0.6",
    author="huansi_mes_team",
    author_email="751995207@qq.com",
    description="rpc服务打包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Click',
        'Flask',
        'google',
        'grpcio',
        'protobuf',
        'soupsieve',
        'six',
    ],
)