from material import Material

class Skin():

    def __init__(self, name: str, materials: List[Material]):
        self._name = name


    def serialize_copy(self, output_path: str) -> None:   
        pass

    def get_name(self) -> str:
        return self._name