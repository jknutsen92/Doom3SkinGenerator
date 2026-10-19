from game_files import MaterialArchive

class Material():
    def parse_material_fragment(path: str) -> MaterialFragment:
        pass

    def __init__(self, name: str, archive: MaterialArchive) -> None:
        self._archive = archive
        self._base_name = name
        material_text = archive.search_material_files(name)
        self._global_keywords = self._parse_globals(material_text)
        self._stages = self._parse_stages(material_text)


    def _parse_globals(self, material_text: str) -> List[str]:
        pass

    
    def _parse_stages(self, material_text: str) -> List[str]:
        pass
    

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