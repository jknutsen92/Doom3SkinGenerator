from material import Material

class Md5mesh():
    def _find_materials(path: str) -> List[str]:
        pass

    def __init__(self, path: str, suffix: str) -> None:
        self._materials = _find_materials(path)
        self._suffix = suffix

    def get_materials(self) -> List[Material]:
        pass