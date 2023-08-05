# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dariah', 'dariah.core', 'dariah.mallet']

package_data = \
{'': ['*']}

install_requires = \
['cophi>=1.3.2,<2.0.0',
 'lda>=1.1.0,<2.0.0',
 'matplotlib>=3.0.3,<4.0.0',
 'numpy>=1.16.2,<2.0.0',
 'pandas>=0.24.2,<0.25.0',
 'regex>=2019.4.12,<2020.0.0',
 'seaborn>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'dariah',
    'version': '2.0.0',
    'description': 'A library for topic modeling and visualization.',
    'long_description': '# A library for topic modeling and visualization\n`dariah` is an easy-to-use Python library for topic modeling and visualization. Getting started is _really easy_. All you have to do is import the library – you can train a model straightaway from raw textfiles.\n\nIt provides two implementations of [latent Dirichlet allocation](http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf):\n- The lightweight, Cython-based package [lda](https://pypi.org/project/lda/)\n- The more robust, Java-based package [MALLET](http://mallet.cs.umass.edu/topics.php)\n\n> Topic modeling algorithms are statistical methods that analyze the words of the original texts to discover the themes that run through them, how those themes are connected to each other, and how they change over time. ([David M. Blei](http://www.cs.columbia.edu/~blei/papers/Blei2012.pdf))\n\n\n## Installation\n```\n$ pip install dariah\n```\n\n\n## Example\n```python\n>>> import dariah\n>>> dariah.topics(directory="british-fiction-corpus",\n...               stopwords=100,\n...               num_topics=10,\n...               num_iterations=1000)\n```\n\n\n## Developing\n[Poetry](https://poetry.eustace.io/) automatically creates a virtual environment, builds and uploads the project to [PyPI](https://pypi.org/). Install dependencies with:\n```\n$ poetry install\n```\n\nrun tests:\n```\n$ poetry run pytest\n```\n\nformat code:\n```\n$ poetry run black dariah\n```\n\nbuild the project:\n```\n$ poetry build\n```\n\nand upload it to [PyPI](https://pypi.org/):\n```\n$ poetry upload\n```\n\n> Save your credentials with `poetry config http-basic.pypi username password`.\n\n\n## About DARIAH-DE\n[DARIAH-DE](https://de.dariah.eu) supports research in the humanities and cultural sciences with digital methods and procedures. The research infrastructure of DARIAH-DE consists of four pillars: teaching, research, research data and technical components. As a partner in [DARIAH-EU](http://dariah.eu/), DARIAH-DE helps to bundle and network state-of-the-art activities of the digital humanities. Scientists use DARIAH, for example, to make research data available across Europe. The exchange of knowledge and expertise is thus promoted across disciplines and the possibility of discovering new scientific discourses is encouraged.\n\nThis software library has been developed with support from the DARIAH-DE initiative, the German branch of DARIAH-EU, the European Digital Research Infrastructure for the Arts and Humanities consortium. Funding has been provided by the German Federal Ministry for Research and Education (BMBF) under the identifier 01UG1610J.\n\n![DARIAH-DE](docs/images/dariah-de_logo.png)\n![BMBF](docs/images/bmbf_logo.png)\n',
    'author': 'DARIAH-DE',
    'author_email': None,
    'url': 'https://dariah-de.github.io/Topics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
