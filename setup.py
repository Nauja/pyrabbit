from setuptools import setup
import os

base_dir = os.path.dirname(__file__)

__pkginfo__ = {}
with open(os.path.join(base_dir, "pysachi", "__pkginfo__.py")) as f:
    exec(f.read(), __pkginfo__)


def install(**kwargs):
    """setup entry point"""
    return setup(
        name="pysachi",
        version=__pkginfo__["version"],
        packages=[
            'pysachi',
            'pysachi/rules',
            'pysachi/checkers'
        ],
        entry_points={'pysachi.renderers': [
            "html = pysachi.renderers.html",
            "raw = pysachi.renderers.raw"
        ]},
        test_suite="pysachi.test",
        python_requires=">=3.4.*",
        setup_requires=["pytest-runner"],
        tests_require=["pytest"],
        **kwargs
    )


if __name__ == "__main__":
    install()
