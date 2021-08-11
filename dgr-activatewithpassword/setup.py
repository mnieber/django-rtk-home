from setuptools import find_packages, setup

setup(
    name="dgr-activatewithpassword",
    version="0.1.0",
    description="Extension of DGR that requires a password in the activation step",
    url="https://github.com/mnieber/dgr-activatewithpassword",
    author="Maarten Nieber",
    author_email="hallomaarten@yahoo.com",
    license="MIT",
    packages=find_packages(),
    package_data={},
    entry_points={},
    data_files=[],
    cmdclass={},
    install_requires=["django-graphql-registration"],
    zip_safe=False,
    python_requires=">=3.6",
)
