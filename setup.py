from setuptools import setup, find_packages

exec(open("kanu/version.py").read())

setup(
    name="kanu",
    version=__version__,
    author='Seung-been "Steven" Lee',
    author_email="sbstevenlee@gmail.com",
    description="KANU",
    url="https://github.com/sbslee/kanu",
    packages=find_packages(),
    install_requires=["openai"],
    license="MIT",
    entry_points={"console_scripts": ["kanu=kanu.__main__:main"]},
    long_description="This is a detailed description of the package.",
    long_description_content_type="text/plain"
)