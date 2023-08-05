# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gencon_miner']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.7,<5.0', 'requests>=2.21,<3.0']

entry_points = \
{'console_scripts': ['jupyter = scripts:jupyter']}

setup_kwargs = {
    'name': 'genconminer',
    'version': '0.1.6',
    'description': 'Wraps Pip packages (beautifulsoup and requests) to a more concise content extractor',
    'long_description': '# Gencon Miner\n\nA general content miner that leverages on Beautiful Soup and Requests to handle extraction. The main goal is to always imagine in terms of targetting parent elements in an HTML form then getting group of tags given that parent.\n\n```python\nfrom gencon_miner import GenconMiner\n```\n\n## From URL\n\n```python\nurl_miner = GenconMiner(url="http://google.com")\ntxt = url_miner.extract(\'title\')\nprint(txt[0].text) # Google\n```\n\n## From text\n\n```python\ntext_miner = GenconMiner(text="<p class=\'myclass\'>Hello</p>")\ntxt = text_miner.extract(\'.myclass\')\nprint(txt[0].text) # Hello\n```\n\n## Convert all tag content to string\n\nNote that contents in a tag will be delimited using newline.\n\n```python\nmeaning_of_life = """\n    <p class=\'myclass\'>\n        Hello\n        <span>darkness my old friend</span>\n    </p>\n    <b>And another one</b>\n"""\nbulk_miner = GenconMiner(text=meaning_of_life)\nprint(bulk_miner.to_text()) # Hello\\ndarkness my old friend\\nAnd another one\n```\n\n## Parent to target\n\nUse-case on walking document and extracting the targets.\n\n```python\nsong_of_the_day = """\n    <table id="mother">\n        <tr>\n            <td class="target-1">Mamma Mia</td>\n            <td class="target-2">Here I go again</td>\n            <td class="target-3">My my</td>\n            <td class="target-4">How can I resist you</td>\n        </tr>\n    </table>\n"""\nwalk_miner = GenconMiner(text=song_of_the_day)\nprint(walk_miner.extract(\'#mother\', \'.target-1\')[0].text) # Mamma Mia\nprint(walk_miner.extract(\'#mother\', \'.target-3\')[0].text) # My my\nprint(walk_miner.extract(\'#mother\', \'td\'))\n# [\n#   <td class="target-1">Mamma Mia</td>,\n#   <td class="target-2">Here I go again</td>,\n#   <td class="target-3">My my</td>,\n#   <td class="target-4">How can I resist you</td>\n# ]\n```\n\n## Author\n\nAlmer Mendoza\n',
    'author': 'Almer Mendoza',
    'author_email': 'amendoza@stratpoint.com',
    'url': 'https://github.com/mamerisawesome/GenconMiner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
