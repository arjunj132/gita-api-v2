# Official Gita API

This Python-Flask based api is powered by BhagavadGita.io AND GitaTeluguAPI.

This is a API designed to proxy out some Gita verses from APIs to provide a consistent format for all languages.

## Other programs

### /api/scripts/languages.py

This [script](https://github.com/arjunj132/gita-api-v2/blob/main/api/scripts/language_scripts.py) provides a clean CLI to find all languages from a JSON file the Gita Foundation's `gita` repository (found in a branch, not in main):

https://raw.githubusercontent.com/gita/gita/feat--new-languages/data/transliteration.json

This file is pretty big, with 6309 entries in the JSON array. This is not currently used for any of our languages, but we belive that we may implement languages such as Tamil later on, using this file.
