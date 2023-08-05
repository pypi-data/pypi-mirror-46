# Gencon Miner

A general content miner that leverages on Beautiful Soup and Requests to handle extraction. The main goal is to always imagine in terms of targetting parent elements in an HTML form then getting group of tags given that parent.

```python
from gencon_miner import GenconMiner
```

## From URL

```python
url_miner = GenconMiner(url="http://google.com")
txt = url_miner.extract('title')
print(txt[0].text) # Google
```

## From text

```python
text_miner = GenconMiner(text="<p class='myclass'>Hello</p>")
txt = text_miner.extract('.myclass')
print(txt[0].text) # Hello
```

## Convert all tag content to string

Note that contents in a tag will be delimited using newline.

```python
meaning_of_life = """
    <p class='myclass'>
        Hello
        <span>darkness my old friend</span>
    </p>
    <b>And another one</b>
"""
bulk_miner = GenconMiner(text=meaning_of_life)
print(bulk_miner.to_text()) # Hello\ndarkness my old friend\nAnd another one
```

## Parent to target

Use-case on walking document and extracting the targets.

```python
song_of_the_day = """
    <table id="mother">
        <tr>
            <td class="target-1">Mamma Mia</td>
            <td class="target-2">Here I go again</td>
            <td class="target-3">My my</td>
            <td class="target-4">How can I resist you</td>
        </tr>
    </table>
"""
walk_miner = GenconMiner(text=song_of_the_day)
print(walk_miner.extract('#mother', '.target-1')[0].text) # Mamma Mia
print(walk_miner.extract('#mother', '.target-3')[0].text) # My my
print(walk_miner.extract('#mother', 'td'))
# [
#   <td class="target-1">Mamma Mia</td>,
#   <td class="target-2">Here I go again</td>,
#   <td class="target-3">My my</td>,
#   <td class="target-4">How can I resist you</td>
# ]
```

## Author

Almer Mendoza
