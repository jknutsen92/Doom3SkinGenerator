from game_files import MaterialArchive
import re

class MaterialFormatError(Exception):
    def __init__(self, message):
        super().__init__(message)
    
    def __str__(self):
        return self.message


class MaterialFragment():
    def __init__(self, material_text: str):
        self._global_keywords = []
        self._stages = []
        self._parse_material(material_text)


    def _parse_material(self, material_text: str) -> None:
        stage_pattern = r"\{[\n\s]+[^\}]+\}|renderbump.+$|diffusemap.+$|bumpmap.+$|specularmap.+$|DECAL_MACRO$"
        self._stages.extend(re.findall(stage_pattern, material_text, re.MULTILINE))
        material_text_sans_stages = re.sub(stage_pattern, '', material_text, 0, re.MULTILINE)
        global_pattern = r"^\S+$"
        self._global_keywords.extend(re.findall(global_pattern, material_text_sans_stages, re.MULTILINE))
    
    def get_globals(self):
        return self._global_keywords


    def get_stages(self):
        return self._stages



class Material(MaterialFragment):
    @staticmethod
    def _strip_enclosing(material_text: str) -> str:
        body_pattern = r"(?<=\{\n)[\s\S]+(?=\n\})"
        if match := re.search(body_pattern, material_text):
            # strip leading whitespace
            return "\n".join(map(str.strip, match.group().splitlines()))
        else:
            raise MaterialFormatError(f"Improperly formatted material: {material_text}")


    def __init__(self, name: str, archive: MaterialArchive) -> None:
        self._archive = archive
        self._name = name
        material_text = archive.search_material_files(name)
        material_text_body = Material._strip_enclosing(material_text)
        super().__init__(material_text_body)


    def __repr__(self) -> str:
        return f"Material:{self.get_name()}"


    def __str__(self) ->str:
        string = ""
        string += f"{self.get_name()} {{\n"
        for global_keyword in self._global_keywords:
            string += f"\t{global_keyword}\n"
        for stage in self._stages:
            for line in stage.splitlines():
                if line.startswith('}') or line.startswith('{'):
                    string += f"\t{line}\n"
                else:
                    string += f"\t\t{line}\n"
        string += "}\n\n"
        return string


    def composite_materials(self, other: Material):
        # Maintain stage order and our stages are before other's
        self._global_keywords += other.get_globals()
        self._stages += other.get_stages()


    def serialize_copy(self, output_path: str, material_suffix: str) -> None:
        print(f"Writing material {self.get_name()} to {output_path}")
        with open(output_path, 'a+') as outfile:
            outfile.write(self.__str__())


    def get_name(self) -> str:
        return self._name


    def set_name(self, name: str) -> None:
        self._name = name