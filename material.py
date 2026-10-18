class Material():
    def parse_material_fragment(path: str) -> MaterialFragment:
        pass

    def __init__(self, name: str, suffix: str):
        self._base_name = name
        self._modified_name = f"{name}_{suffix}"

    def append_material_fragment(self, fragment: MaterialFragment):
        pass

    def serialize_copy(self, output_path: str, material_suffix: str) -> None:
        pass

    def get_base_name(self) -> str:
        return self._base_name

    def get_modified_name(self) -> str:
        return self._modified_name

class MaterialFragment():
    pass