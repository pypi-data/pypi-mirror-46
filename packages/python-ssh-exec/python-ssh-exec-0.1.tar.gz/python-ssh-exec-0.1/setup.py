from setuptools import setup

setup(
    name="python-ssh-exec",
    version="0.1",
    py_modules=["python-ssh-exec"],
    install_requires=["Click==7.0", "paramiko==2.4.2", "cryptography==2.4.2"],
    entry_points="""
        [console_scripts]
        pyssh=pysshexec:main
    """,
)
