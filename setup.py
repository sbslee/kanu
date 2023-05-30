from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text()

exec(open("kanu/version.py").read())

setup(
    name="kanu",
    version=__version__,
    author='Seung-been "Steven" Lee',
    author_email="sbstevenlee@gmail.com",
    description="A minimalistic Python-based GUI for various chatbots",
    url="https://github.com/sbslee/kanu",
    packages=find_packages(),
    license="MIT",
    entry_points={"console_scripts": ["kanu=kanu.__main__:main"]},
    long_description=long_description,
    long_description_content_type="text/markdown"
)