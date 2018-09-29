class _FormatDict(object):
    def __init__(self, initial=None):
        self._dict = {}
        if initial:
            self._dict = initial

    def __getitem__(self, item):
        if item in self._dict.values():
            return item
        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def match(self, content_type):
        return len([
            key
            for key, value in self._dict.items()
            if key == content_type
        ]) > 0


JsonLd = "JsonLd"
Hydra = "hydra"
Formats = _FormatDict({
    "application/ld+json": JsonLd,
    "application/json": JsonLd,
})
