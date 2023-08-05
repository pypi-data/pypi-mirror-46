from setuptools import setup, find_packages

setup(
    name="adApkTools",
    version="1.0.5",
    keywords=["channel", "adApkTools", "apk channel"],
    description="An ad channel apk generator",
    long_description="An ad channel apk generator used for chinese android ad package.",
    license="MIT Licence",

    url="https://github.com/Carlos-Zen/adApkTools",
    author="CarlosZen",
    author_email="lianmezhi@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any"
)
