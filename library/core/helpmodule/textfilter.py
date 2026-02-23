import requests

from urllib.parse import quote_plus

from library.core import console

api = "https://www.purgomalum.com/service/json?text={text}&fill_char=_"

def FilterStringAsync(RawText:str) -> str:
    try:
        response = requests.get(
            url=api.format(text=quote_plus(RawText)),
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            return data.get('result', RawText).replace('_', '#')
        else:
            return RawText
    except Exception as e:
        console.warn(f"Something Went Wrong While Filtering Text: {e}")
        return RawText