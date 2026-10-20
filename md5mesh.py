from material import Material
from game_files import MaterialArchive
import re

class Md5mesh():
    @staticmethod
    def _find_materials(path: str) -> List[str]:
        shader_pattern = r"shader\s+\"([^\"]+)"
        with open(path) as md5mesh_file:
            shader_names = map(lambda x: x.groups()[0], re.finditer(shader_pattern, md5mesh_file.read()))
            material_names = [t for t in shader_names if Md5mesh._is_material(t)]
            return material_names

    def _is_material(material: str) -> bool:
        common_pattern = r"textures/common/.+"
        if re.match(common_pattern, material):
            return False
        return True

    def __init__(self, path: str, archive: MaterialArchive) -> None:
        self._archive = archive
        self._materials = Md5mesh._find_materials(path)

    def get_materials(self) -> List[Material]:
        materials = []
        for material_name in self._materials:
            materials.append(Material(material_name, self._archive))
        return materials