from setuptools import find_packages, setup

setup(
    name="django-rtk-blue",
    version="0.5.0",
    description="Extension of django-rtk that combines django-rtk-upfront, django-rtk-password and django-rtk-magic-link",
    long_description="Extension of django-rtk that combines django-rtk-upfront, django-rtk-password and django-rtk-magic-link",
    long_description_content_type="text/x-rst",
    url="https://github.com/mnieber/django-rtk-home/blob/main/django-rtk-blue/README.md",
    author="Maarten Nieber",
    author_email="hallomaarten@yahoo.com",
    license="MIT",
    packages=find_packages(),
    package_data={},
    entry_points={},
    data_files=[],
    cmdclass={},
    install_requires=[
        "django-rtk",
        "django-rtk-upfront",
        "django-rtk-password",
        "django-rtk-magic-link",
    ],
    zip_safe=False,
    python_requires=">=3.6",
)
