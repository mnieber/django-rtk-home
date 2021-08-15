from setuptools import find_packages, setup

setup(
    name="django-rtk-green",
    version="0.1.0",
    description="Extension of DGR that requires a password in the activation step",
    url="https://github.com/mnieber/django-rtk-green",
    author="Maarten Nieber",
    author_email="hallomaarten@yahoo.com",
    license="MIT",
    packages=find_packages(),
    package_data={},
    entry_points={},
    data_files=[],
    cmdclass={},
    install_requires=["django-rtk"],
    zip_safe=False,
    python_requires=">=3.6",
)
