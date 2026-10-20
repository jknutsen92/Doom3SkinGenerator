import re
from game_files import EntityArchive, MeshMissingError
from typing import Optional

class SkinMissingError(Exception):
    def __init__(self, message):
        super().__init__(message)
    
    def __str__(self):
        return self.message


class EntityDef():       

    @staticmethod
    def _get_parent_entity(entity_def_text: str) -> bool:
        inherit_pattern = r"inherit\"\s+\"([^\"]+)"
        if match := re.search(inherit_pattern, entity_def_text):
           return match.groups()[0] 
        return None

    
    def __init__(self, name: str, archive: EntityArchive) -> None:
        self._archive = archive
        entity_def_text = archive.search_entity_files(name)
        self._name = name
        self._head = self._find_head(entity_def_text)
        self._skin = self._find_skin(entity_def_text)


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
        entity_def_text = self._archive.search_entity_files(self._name)
        if path := self._find_md5_mesh_path(entity_def_text):
            return path        
        elif parent_name := EntityDef._get_parent_entity(entity_def_text):
            parent = EntityDef(parent_name, self._archive)
            return parent.get_mesh_path()
        else:
            raise MeshMissingError(f"No mesh found in the inheritance hierarchy for {self.get_name()}")
            

    def get_name(self) -> str:
        return self._name


    def is_child(self) -> bool:
        if not self._md5mesh_path and self._skin:
            return True
        return False


    def has_skin(self) -> bool:
        return not self._skin is None


    def get_skin_name(self) -> str:
        return self._skin
    

    def _find_head(self, entity_def_text: str) -> Optional[HeadEntityDef]:
        head_def_pattern = r"def_head\"\s+\"([^\"]+)"
        if match := re.search(head_def_pattern, entity_def_text):
            head_model_def = match.groups()[0]
            print(f"Found head model for {self._name}: {head_model_def}")
            mesh_path = self._archive.search_model_def_files(head_model_def)
            return HeadEntityDef(head_model_def, self._archive)
        return None


    def _find_md5_mesh_path(self, entity_def_text: str) -> Optional[str]:
        model_name_pattern = r"model\"\s+\"(.+)\""
        if model_match := re.search(model_name_pattern, entity_def_text):
            model_name = model_match.groups()[0]
            model_def_text = self._archive.search_model_def_files(model_name)
            return self._parse_md5_mesh_path(model_def_text)
        return None


    def _parse_md5_mesh_path(self, model_def_text: str) -> str:
        mesh_pattern = r"mesh\s+(\S+)"
        if match := re.search(mesh_pattern, model_def_text):
            return match.groups()[0]
        else:
            return None


    def _find_skin(self, entity_def_text: str) -> str:
        # Recursively search entity def, model defs, and any entity defs or model defs we inherit from
        skin_pattern = r"skin\"\s+\"([^\"]+)\.skin"
        model_pattern = r"model\"\s+\"([^\"]+)"
        inherit_pattern = r"inherit\"\s+\"([^\"]+)"
        # Try searching in the entityDef first
        if match := re.search(skin_pattern, entity_def_text):
            return match.groups()[0]
        # Sometimes skins are defined in the model def
        if match := re.search(model_pattern, entity_def_text):
            model_skin = self._find_model_skin_name(match.groups()[0])
            if model_skin:
                return model_skin
        # Check our parent entity def and model for the skin
        if match := re.search(inherit_pattern, entity_def_text):
            parent_entity_def_text = self._archive.search_entity_files(match.groups()[0])
            return self._find_skin(parent_entity_def_text)
        return None


    def _find_model_skin_name(self, model_name: str) -> str:
        model_def_text = self._archive.search_model_def_files(model_name)
        skin_pattern = r"skin\s+(\S+)\.skin"
        inherit_pattern = r"inherit\s+(\S+)"
        # Check our model def for a skin reference
        if match := re.search(skin_pattern, model_def_text):
            return match.groups()[0]
        # If our model inherits from another model, search that one
        elif match := re.search(inherit_pattern, model_def_text):
            parent_model_name = match.groups()[0]
            return self._find_model_skin_name(parent_model_name)
        else:
            return None


class HeadEntityDef(EntityDef):
    def __init__(self, model_name: str, archive: EntityArchive):
        self._archive = archive
        model_def_text = archive.search_model_def_files(model_name)
        self._name = model_name
        self._head = None
        self._mesh_path = self._find_mesh_path(model_def_text)
        self._skin = self._find_skin_name(model_def_text)

    
    def _find_mesh_path(self, model_def_text: str) -> str:
        mesh_pattern = r"mesh\s+(\S+\.md5mesh)"
        if match := re.search(mesh_pattern, model_def_text):
            return match.groups()[0]
        else:
            raise MeshMissingError(f"Head model def {self._name} doesn't have a declared mesh")

    
    def _find_skin_name(self, model_def_text: str) -> str:
        skin_pattern = r"skin\s+(\S+)\.skin"
        if match := re.search(skin_pattern, model_def_text):
            return match.groups()[0]
        else:
            return None


    def get_mesh_path(self) -> str:
        return self._mesh_path