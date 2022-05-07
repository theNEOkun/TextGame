class World_Cell:
    coords: tuple
    description: dict
    items: dict
    interactions: dict
    mapping: str


    def __str__(self) -> dict:
        return {"coords": self.coords,
                "description": self.description,
                "items": self.items,
                "interactions": self.interactions,
                "mapping": self.mapping
                }


    def __init__(self, coords, descr, items, interact, mapp):
        self.coords = coords
        self.description = descr
        self.items = items
        self.interactions = interact
        self.mapping = mapp
