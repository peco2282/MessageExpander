import re

from setuptools import setup

with open("README.md", mode="r", encoding="utf8") as f:
    description = f.read()


with open("expander/__init__.py", mode="r", encoding="utf8") as f:
    search = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)

    if search is not None:
        version = search.group(1)

setup(
    name='expander',
    version=version or "1.0.0",
    packages=['expander'],
    long_description=description,
    long_description_content_type="text/markdown",
    url='https://github.com/peco2282/expander',
    license='MIT',
    author='peco2282',
    author_email='pecop2282@gmail.com',
    description='expand discord message links',
    requires=[
        "py-cord>=2.0.0b1"
    ]
)
