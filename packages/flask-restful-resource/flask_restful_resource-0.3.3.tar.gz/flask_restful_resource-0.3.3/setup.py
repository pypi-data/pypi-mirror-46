from setuptools import find_packages, setup

setup(
    name="flask_restful_resource",
    version="0.3.3",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask==1.0.2",
        "Flask-RESTful==0.3.6",
        "schema==0.6.8",
        "marshmallow==2.16.3",
        "requests==2.19.1",
        "kazoo==2.5.0",
        # mongo
        # "marshmallow-mongoengine==0.9.1",
        # "flask-mongoengine==0.9.5",
        # sql
        # "Flask-SQLAlchemy==2.3.2",
        # "flask-marshmallow==0.9.0",
        # "marshmallow-sqlalchemy==0.15.0",
    ],
)
