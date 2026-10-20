from material import Material
from game_files import SkinArchive
import re

class Skin():
    @staticmethod
    def _parse_materials_mapping(skin_def: str) -> dict[str,str]:
        mat_map = {}
        map_pattern = r"(?<!//)(models\S+)\s+(\S+)"
        for match in re.finditer(map_pattern, skin_def):
            mat_map[match.groups()[0]] = match.groups()[1]
        return mat_map

    
    def __init__(self, name: str, material_mapping: dict[str,str], skin_archive: SkinArchive = None) -> None:
        self._archive = skin_archive
        self._name = name
        if material_mapping is None:
            skin_def = self._archive.search_skin_files(name)
            self._materials_mapping = Skin._parse_materials_mapping(skin_def)
        else:
            self._materials_mapping = material_mapping

    
    def __repr__(self) -> str:
        return f"Skin:{self.get_name()}"

    
    def __str__(self) -> str:
        string = ""
        string += f"skin {self.get_name()} {{\n"
        for source_material, override_material in self._materials_mapping.items():
            string += f"\t{source_material}\t\t\t{override_material}\n"
        string += "}\n\n"
        return string

    
    def get_source_materials(self) -> str:
        materials = []
        for material_name in self._materials_mapping.keys():
            material = Material(material_name)
        return materials


    def serialize_copy(self, output_path: str) -> None:   
        print(f"Writing skin {self.get_name()} to {output_path}")
        with open(output_path, 'a+') as outfile:
            outfile.write(self.__str__())


    def get_name(self) -> str:
        return self._name


    def is_no_draw_skin(self):
        for material_remap in self._materials_mapping.values():
            if material_remap != "textures/common/nodraw":
                return False
        return True


    def material_overridden_with_common_texture(self, material_name: str):
        common_pattern = r"textures/common/.+"
        if material_name in self._materials_mapping:
            if re.match(common_pattern, self._materials_mapping[material_name]):
                return True
        return False


    def get_overriden_material(self, material_name: str) -> str:
        if material_name in self._materials_mapping:
            return self._materials_mapping[material_name]
        return None    