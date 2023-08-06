import ast
import re
from setuptools import setup, find_packages

from pathlib import Path


CURRENT_DIR = Path(__file__).parent


def get_version() -> str:
    main_py = CURRENT_DIR / "sqlvalidator" / "main.py"
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(main_py, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
        return str(ast.literal_eval(version))


def get_long_description() -> str:
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


setup(
    name="sqlvalidator",
    version=get_version(),
    description="SQL queries formatting (and soon basic schema less validation)",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/David-Wobrock/sqlvalidator",
    author="David Wobrock",
    author_email="david.wobrock@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["tests/"]),
    python_requires=">=3.6",
    install_requires=["sqlparse==0.3.0"],
    keywords="python sql format formatter formatting validation validator validate automation",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
    ],
    entry_points={"console_scripts": ["sqlvalidator = sqlvalidator.main:_main"]},
)
