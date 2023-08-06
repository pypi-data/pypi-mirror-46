import botocore

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

files = ["static/css/*", "rawdata/*", "templates/*", "static/js/*", "static/scss/*", "static/vendor/bootstrap/*","static/js/demo/*",
         "static/vendor/chart.js/*", "static/vendor/datatables/*", "static/vendor/fontawesome-free/*", "static/vendor/jquery/*"
         ,"static/vendor/jquery-easing/*", "static/vendor/bootstrap/css/*", "static/vendor/bootstrap/js/*", "static/vendor/fontawesome-free/css/*",
         "static/vendor/fontawesome-free/js/*", "static/vendor/fontawesome-free/less/*", "static/vendor/fontawesome-free/scss/*", "static/vendor/fontawesome-free/sprites/*",
         "static/vendor/fontawesome-free/svgs/*", "static/vendor/fontawesome-free/webfonts/*"]

setuptools.setup(
    name="testmodelkb1",
    version="3.0.8",
    author="Sirisha Rella",
    author_email="srnk2@mail.umkc.edu",
    description="ModelKB",
    long_description="ModelKB",
    long_description_content_type="text/markdown",
    url="https://github.com/SirishaRella/Xsequential_package",
    package_data={'Xsequential': files},
    packages=['Xsequential'],
    include_package_data=True,
    install_requires=['Flask'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)