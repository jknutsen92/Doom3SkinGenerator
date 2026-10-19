import re
from game_files import EntityArchive, MeshMissingError
from typing import Optional

class EntityDef():       

    @staticmethod
    def _is_a_child_entity(entity_def_text: str) -> bool:
        inherit_pattern = r"inherit\"\s+\"([^\"]+)"
        if re.search(inherit_pattern, entity_def_text):
           return True 
        return False


    @staticmethod
    def _find_skin(entity_def_text: str) -> str:
        skin_pattern = r"skin\"\s+\"([^\"]+)\.skin"
        if match := re.search(skin_pattern, entity_def_text):
            return match.groups()[0] 

    
    def __init__(self, name: str, archive: EntityArchive) -> None:
        self._archive = archive
        entity_def_text = archive.search_entity_files(name)
        self._name = name
        self._head = self._find_head(entity_def_text)
        try:
            self._md5mesh_path = self._find_md5_mesh_path(entity_def_text)
            self._skin = None
        except MeshMissingError:
            if EntityDef._is_a_child_entity(entity_def_text):
                self._md5mesh_path = None
                self._skin = EntityDef._find_skin(entity_def_text)
                print(f"{self._name} doesn't have its own mesh defined. Skin {self._skin} overrides materials")
            else:
                raise MeshMissingError(f"Entity def {self._name} is missing a mesh and doesn't inherit. Invalid definition")


    def __str__(self) -> str:
        return f"EntityDef:name={self._name},head={self._head},md5mesh={self._md5mesh_path}"


    def __repr__(self) -> str:
        return f"EntityDef:{self._name}"


    def has_head(self):
        if self._head:
            return True
        return False


    def get_head(self):
        return self._head


    def get_mesh_path(self) -> str:
        return self._md5mesh_path


    def get_name(self) -> str:
        return self._name


    def is_child(self) -> bool:
        if not self._md5mesh_path and self._skin:
            return True
        return False

    def get_skin_name(self) -> str:
        return self._skin
    
    def _find_head(self, entity_def_text: str) -> Optional[HeadEntityDef]:
        head_def_pattern = r"def_head\"\s+\"([^\"]+)"
        if match := re.search(head_def_pattern, entity_def_text):
            head_model_def = match[1]
            print(f"Found head model for {self._name}: {head_model_def}")
            mesh_path = self._archive.search_model_def_files(head_model_def)
            return HeadEntityDef(head_model_def, mesh_path)
        return None


    def _find_md5_mesh_path(self, entity_def_text: str) -> str:
        model_name_pattern = r"model\"\s+\"(.+)\""
        if model_match := re.search(model_name_pattern, entity_def_text):
            model_name = model_match.groups()[0]
            return self._archive.search_model_def_files(model_name)
        raise MeshMissingError(f"No md5 mesh reference found in {self._name}")

        

class HeadEntityDef():
    def __init__(self, name, mesh_path: str):
        self._name = name
        self._md5mesh_path = mesh_path


    def __repr__(self) -> str:
        return f"EntityDef:{self._name}"


    def get_name(self) -> str:
        return self._name


    def get_mesh_path(self) -> str:
        return self._md5mesh_path
