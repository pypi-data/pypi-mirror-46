from setuptools import setup, find_packages

setup(
    name="drf_jwt_util",
    version="0.1.5",
    description="drf jwt util",
    author='Shunsuke Aihara',
    author_email='aihara@argmax.jp',
    url='https://github.com/shunsukeaihara/drf_jwt_util',
    packages=find_packages(),
    include_package_data=True,
    install_requires=["django", "djangorestframework", "djangorestframework-jwt", "social-auth-app-django"],
    tests_require=["tox", "factory_boy", "faker>=1.0.6"],
    license="MIT License",
)
