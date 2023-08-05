import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ascii_films",
    version="0.0.18",
    author="Robert Sebille",
    author_email="robert@sebille.name",
    maintainer = 'Robert Sebille',
    maintainer_email = 'robert@sebille.name',
    description="Cette classe fournit des outils pour afficher des petits\
 films à partir de frames en ascii.",
    license="GNU GPL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://framagit.org/zenjo/film/wikis/home",
    download_url = 'https://framagit.org/zenjo/film/tree/master',
    #packages=setuptools.find_packages(),
    #py_modules = ['film', 'demo'],
    packages = ['film'],
    package_data={
        'film': ['frame/*', 'frames/*'],
    },
    #data_files = [('frame',['frame/poursuiteic', 'frame/poursuiteci', 'frame/roflflyingmoto']),
    #              ('frames',['frames/bon00', 'frames/bon10', 'frames/bon20', 'frames/bon30'])],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent",
    ],
)
