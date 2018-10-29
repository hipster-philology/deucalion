import requests
from .models import Model


class PieWebApp(Model):
    def __init__(self, uri, *args, **kwargs):
        super(PieWebApp, self).__init__(*args, **kwargs)
        self._uri = uri

    def lemmatize(self, text) -> str:
        req = requests.post(
            self._uri,
            data={"data": text}
        )
        req.raise_for_status()
        return req.text
