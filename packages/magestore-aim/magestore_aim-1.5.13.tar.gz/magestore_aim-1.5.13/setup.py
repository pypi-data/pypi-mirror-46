import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

package_name = 'magestore_aim'
packages = setuptools.find_packages(include=[package_name, "{}.*".format(package_name)])

setuptools.setup(
    name=package_name,
    version="1.5.13",
    author="Mars",
    author_email="mars@trueplus.vn",
    description="Install zend-barcode module",
    long_description=long_description,
    long_description_content_type="",
    url="https://magestore.com",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3',
    install_requires=[
        # install specific crytography 2.4.2 to fix error with 2.5 version
        # ref: https://github.com/paramiko/paramiko/issues/1369
        'cryptography==2.4.2',
        'fabric',
        'packaging'
    ],
    include_package_data=True
)
