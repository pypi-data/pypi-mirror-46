import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "glstatus",
    packages = ["glstatus"],
    entry_points = {
        "console_scripts": ['glstatus = glstatus.glstatus:main']
        },
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "1.0.1",
    description = "A simple tool to retrieve and update your GitLab status from your terminal",
    author = "Yoginth",
    author_email = "me@yoginth.com",
    url = "https://yoginth.com",
    classifiers=(
        "Programming Language :: Python",
        "Natural Language :: English",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
    ),
    project_urls={
        'Patreon': 'https://www.patreon.com/yoginth',
        'Source': 'https://gitlab.com/yoginth/glstatus',
    },
    install_requires=[
        'requests',
        'emojis'
    ],
)
