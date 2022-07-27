from setuptools import find_packages, setup

setup(
    name="django-rtk",
    version="0.5.0",
    description="Abstract basis for registrating Django users using graphql",
    long_description="Abstract basis for registrating Django users using graphql",
    long_description_content_type="text/x-rst",
    url="https://github.com/mnieber/django-rtk-home/blob/main/django-rtk/README.md",
    author="Maarten Nieber",
    author_email="hallomaarten@yahoo.com",
    license="MIT",
    packages=find_packages(),
    package_data={},
    entry_points={},
    data_files=[],
    cmdclass={},
    install_requires=[
        "Django",
        "graphene-django",
        "django-graphql-jwt",
        "django-templated-mail",
    ],
    zip_safe=False,
    python_requires=">=3.6",
)
