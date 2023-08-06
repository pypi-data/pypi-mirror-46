import subprocess
from codecs import open
from setuptools import setup, find_packages
from setuptools.command import develop, build_py
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


def readme():
    with open("README.md", "r", "utf-8") as f:
        return f.read()


class CustomDevelop(develop.develop, object):
    """
    Class needed for "pip install -e ."
    """
    def run(self):
        subprocess.check_call("make", shell=True)
        super(CustomDevelop, self).run()


class CustomBuildPy(build_py.build_py, object):
    """
    Class needed for "pip install s2p"
    """
    def run(self):
        super(CustomBuildPy, self).run()
        subprocess.check_call("make", shell=True)
        subprocess.check_call("cp -r bin lib build/lib/", shell=True)


class BdistWheel(_bdist_wheel):
    """
    Class needed to build platform dependent binary wheels
    """
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False


requirements = ['numpy',
                'scipy',
                'rasterio[s3,test]',
                'utm',
                'pyproj',
                'beautifulsoup4[lxml]',
                'ransac',
                'requests']

setup(name="s2p",
      version="1.0b12",
      description="Satellite Stereo Pipeline.",
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='https://github.com/cmla/s2p',
      packages=['s2p'],
      install_requires=requirements,
      cmdclass={'develop': CustomDevelop,
                'build_py': CustomBuildPy,
                'bdist_wheel': BdistWheel},
      entry_points="""
          [console_scripts]
          s2p=s2p.cli:main
      """)
