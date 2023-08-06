import re
import json

import requests

from altoshift.search import SearchApi

API_KEY = None

DEV = False

class SearchEngine():
    """
    SearchEngine's basic api management object
    - CRUD operations to search engine's indexed items
    - processing of the search engine's feeds
    - make search requests
    """
    @classmethod
    def test(hei):
        hei = hei+'haa'
        return hei