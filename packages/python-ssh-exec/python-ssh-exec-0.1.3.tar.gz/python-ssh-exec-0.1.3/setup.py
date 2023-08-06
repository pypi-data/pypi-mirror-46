from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="python-ssh-exec",
    version="0.1.3",
    author="AdamGold",
    author_email="adamgold7@gmail.com",
    description="A library to execute local python scripts on remote servers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdamGold/python-ssh-exec",
    py_modules=["pysshexec"],
    install_requires=["Click==7.0", "paramiko==2.4.2", "cryptography==2.4.2"],
    entry_points="""
        [console_scripts]
        pyssh=pysshexec:main
    """,
)
