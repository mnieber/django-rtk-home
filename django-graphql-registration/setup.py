from setuptools import find_packages, setup

setup(
    name="django-graphql-registration",
    version="0.1.0",
    description="Abstract basis for registrating Django users using graphql",
    url="https://github.com/mnieber/django-graphql-registration",
    author="Maarten Nieber",
    author_email="hallomaarten@yahoo.com",
    license="MIT",
    packages=find_packages(),
    package_data={},
    entry_points={},
    data_files=[],
    cmdclass={},
    install_requires=["Django", "graphene-django"],
    zip_safe=False,
    python_requires=">=3.6",
)
