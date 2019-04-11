from setuptools import setup
import os

base_dir = os.path.dirname(__file__)

__pkginfo__ = {}
with open(os.path.join(base_dir, "pyrabbit", "__pkginfo__.py")) as f:
    exec(f.read(), __pkginfo__)


def install(**kwargs):
    """setup entry point"""
    return setup(
        name="pyrabbit",
        version=__pkginfo__["version"],
        packages=[
            'pyrabbit'
        ],
        test_suite="test",
        python_requires=">=3.4.*",
        setup_requires=["pytest-runner"],
        tests_require=["pytest"],
        **kwargs
    )


if __name__ == "__main__":
    install()
