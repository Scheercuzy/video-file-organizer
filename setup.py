from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="Video File Organizer",
    version="2",
    python_requires=">=3.6",
    description="""Organizes the video files in the correct directories""",
    long_description=readme(),
    url="https://github.com/Scheercuzy/video_file_organizer",
    author="MX",
    author_email="maxi730@gmail.com",
    license="MIT",
    install_requires=[
        "appdirs==1.4.4",
        "attrs==19.3.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "babelfish==0.5.5",
        "black==19.10b0; python_version >= '3.6'",
        "cached-property==1.5.1",
        "cerberus==1.3.2",
        "certifi==2020.6.20",
        "chardet==3.0.4",
        "click==7.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "colorama==0.4.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "distlib==0.3.1",
        "flask==1.1.2",
        "guessit==3.1.1",
        "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "importlib-metadata==1.7.0; python_version < '3.8'",
        "itsdangerous==1.1.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "jaraco.functools==3.0.1; python_version >= '3.6'",
        "jinja2==2.11.2",
        "markupsafe==1.1.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "more-itertools==8.4.0; python_version >= '3.5'",
        "orderedmultidict==1.0.1",
        "packaging==20.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pathspec==0.8.0",
        "pep517==0.8.2",
        "pip-shims==0.5.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "pipenv-setup==3.1.1",
        "pipfile==0.0.2",
        "plette[validation]==0.2.3; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pyaml==20.4.0",
        "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pytz==2020.1",
        "pyyaml==5.3.1",
        "rebulk==2.0.1",
        "regex==2020.7.14",
        "requests==2.24.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "requirementslib==1.5.12; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "tempora==4.0.0; python_version >= '3.6'",
        "toml==0.10.1",
        "tomlkit==0.6.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "typed-ast==1.4.1",
        "typing==3.7.4.3; python_version < '3.7'",
        "urllib3==1.25.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
        "uwsgi==2.0.19.1",
        "vistir==0.5.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "werkzeug==1.0.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "wheel==0.34.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "yg-lockfile==2.3",
        "zc.lockfile==2.0",
        "zipp==3.1.0; python_version < '3.8'",
    ],
    dependency_links=[],
    packages=["video_file_organizer"],
    include_package_data=True,
    entry_points={"console_scripts": ["vfo = video_file_organizer.__main__:main"]},
)