from material import Material
from game_files import SkinArchive
import re

class Skin():
    @staticmethod
    def _parse_materials(skin_def: str) -> dict[str,str]:
        mat_map = {}
        map_pattern = r"(?<!//)(models\S+)\s+(\S+)"
        for match in re.finditer(map_pattern, skin_def):
            mat_map[match.groups()[0]] = match.groups()[1]
        return mat_map

    
    def __init__(self, name: str, skin_archive: SkinArchive) -> None:
        self._archive = skin_archive
        self._name = name
        skin_def = self._archive.search_skin_files(name)
        self._materials_mapping = Skin._parse_materials_mapping(skin_def)

    
    def get_source_materials(self) -> str:
        return self._materials_mapping.keys()

    def serialize_copy(self, output_path: str) -> None:   
        pass

    def get_name(self) -> str:
        return self._name

    def is_no_draw_skin(self):
        for material_remap in self._materials_mapping.values():
            if material_remap != "textures/common/nodraw":
                return False
        return True