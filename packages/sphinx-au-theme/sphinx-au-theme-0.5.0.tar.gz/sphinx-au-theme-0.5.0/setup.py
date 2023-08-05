from setuptools import setup

setup(
    name="sphinx-au-theme",
    version="0.5.0",
    author="Dan Søndergaard",
    author_email="das@birc.au.dk",
    description="Sphinx theme emulating pages from Aarhus University, Denmark.",
    entry_points={
        "sphinx.html_themes": [
            "au = sphinx_au_theme",
        ]
    },
    zip_safe=False,
    packages=['sphinx_au_theme'],
    package_data={'sphinx_au_theme': [
        'theme.conf',
        '*.html',
        'static/css/*.css',
        'static/favicon.ico',
        'static/font/*.*'
    ]},
    include_package_data=True,
    install_requires=["sphinx"],
)

