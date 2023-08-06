from setuptools import setup, find_packages

setup(
    name="funki-io-ui",
    version="1.0",
    description="Custom frontend for Home Assisten",
    url="https://github.com/sumitdocument/home-assistant-polymer",
    author="Sumit Tripathi",
    author_email="tr.sumit@gmail.com",
    license="Apache License 2.0",
    packages=find_packages(include=["hass_frontend", "hass_frontend.*"]),
    include_package_data=True,
    zip_safe=False,
)
