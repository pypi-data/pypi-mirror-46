
class UnknownLink:
    def __init__(self, link: str):
        self.short = link.split('#')[0]
        self.long = link

    def __str__(self) -> str:
        return self.long
