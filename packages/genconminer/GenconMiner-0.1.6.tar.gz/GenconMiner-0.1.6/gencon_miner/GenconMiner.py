import requests
from bs4 import BeautifulSoup
from .exceptions import NoInputForProcessing, InputOverloadForProcessing, UrlContentNotAccessible

class GenconMiner:
    def __init__(self, url: str=None, text: str=None) -> None:
        if url is None and text is None:
            raise NoInputForProcessing('Should either have url=<str> or text=<str>')

        if url and text:
            raise InputOverloadForProcessing('Having both set is anti-pattern; consider using either but not both')

        self.url = url
        self.text = text

    def _get_html_data(self) -> None:
        html_data = requests.get(self.url)
        if not html_data or html_data.status_code > 400:
            raise UrlContentNotAccessible('Cannot access url: {}'.format(self.url))

        self.text = html_data.text

    def _extract_from_url(self, parent: str, target: str=None) -> list:
        self._get_html_data()
        return self._extract_from_text(parent, target)

    def _extract_from_text(self, parent: str, target: str=None) -> list:
        bs_txt = BeautifulSoup(self.text, 'html.parser')
        if target is not None:
            parent_txt = bs_txt.select_one(parent)
            return parent_txt.select(target)

        parent_txt = bs_txt.select(parent)
        return parent_txt

    def extract(self, parent: str, target: str=None) -> list:
        if self.url:
            return self._extract_from_url(parent, target)

        if self.text:
            return self._extract_from_text(parent, target)

        raise NoInputForProcessing('Should either have url=<str> or text=<str> on initialization')

    def to_text(self) -> str:
        if self.url and not self.text:
            self._get_html_data()

        if not hasattr(self, 'soup'):
            self.soup = self.text

        if not isinstance(self.soup, BeautifulSoup):
            self.soup = BeautifulSoup(self.text, 'html.parser')

        [s.extract() for s in self.soup(['script', 'style'])]
        return self.soup.get_text("\n", strip=True)

    def to_soup(self) -> str:
        if self.url and not self.text:
            self._get_html_data()

        if hasattr(self, 'soup'):
            return self.soup

        self.soup = self.text
        if not isinstance(self.text, BeautifulSoup):
            self.soup = BeautifulSoup(self.text, 'html.parser')

        return self.soup
