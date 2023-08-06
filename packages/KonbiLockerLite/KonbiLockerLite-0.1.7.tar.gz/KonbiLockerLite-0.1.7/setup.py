import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install
from pathlib import Path


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        Path("ok.txt").write_text("test")
        install.run(self)


setuptools.setup(
    name="KonbiLockerLite",
    version="0.1.7",
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(),
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand
    },
)
