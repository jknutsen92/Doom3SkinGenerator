import re
from glob import glob

class EntityMissingError(Exception):
    def __init__(self, message):
        super().__init__(message)
    
    def __str__(self):
        return self.message

class MeshMissingError(Exception):
    def __init__(self, message):
        super().__init__(message)
    
    def __str__(self):
        return self.message
    
class SkinMissingError(Exception):
    def __init__(self, message):
        super().__init__(message)
    
    def __str__(self):
        return self.message


class EntityArchive():

    @staticmethod
    def _get_def_files(path: str) -> List[str]:
        globs = glob(f"{path}/def/*.def")
        print(f"Found {len(globs)} def files")
        return globs

    @staticmethod
    def _get_mesh_path_from_model_def(model_def_text: str) -> str:
        mesh_path_pattern = r"mesh\s+(\S+\.md5mesh)"
        if result := re.search(mesh_path_pattern, model_def_text):
            return result.groups()[0]
        else:
            raise MeshMissingError("No mesh reference found")

    def __init__(self, path: str) -> None:
        self._base_path = path
        self._entity_def_index = {}
        self._model_def_index = {}
        self._def_files_to_walk = EntityArchive._get_def_files(path)

    
    def _walk_entity_def_files(self, target_entity = None, target_model = None) -> None:
        files_visited = []
        for def_file in self._def_files_to_walk:
            with open(def_file) as def_file_body:
                def_file_body = def_file_body.read()
                entity_defs = self._get_entity_defs(def_file_body)
                model_defs = self._get_model_defs(def_file_body)
                print(f"Found {len(entity_defs)} entity definitions in {def_file}")
                print(f"Found {len(model_defs)} model definitions in {def_file}")
            files_visited.append(def_file)
            if target_entity and target_entity in self._entity_def_index:
                print(f"Found {target_entity} in {def_file}")
                break
            if target_model and target_model in self._model_def_index:
                print(f"Found {target_model} in {def_file}")
                break
        
        print(f"Indexed {len(files_visited)} def file(s)")
        # Remove the files we've already walked
        self._def_files_to_walk = [f for f in self._def_files_to_walk if f not in files_visited]


    def search_entity_files(self, entity_name: str) -> str:
        # If we have the entity def cached already, return that
        if entity_name in self._entity_def_index:
            return self._entity_def_index[entity_name]

        self._walk_entity_def_files(entity_name)
        
        if entity_name in self._entity_def_index:
            return self._entity_def_index[entity_name]        
        else:
            raise IOError(f"{entity_name} not found in {self._base_path}/def")


    def search_model_def_files(self, model_name: str) -> str:
        if model_name in self._model_def_index:
            return self._model_def_index[model_name]

        self._walk_entity_def_files(None, model_name)

        if model_name in self._model_def_index:
            return self._model_def_index[model_name]
        else:
            raise MeshMissingError(f"model {model_name} not found in {self._base_path}/def")

    def get_base_path(self) -> str:
        return self._base_path


    def _get_entity_defs(self, def_file_text: str) -> List[str]:
        entity_def_pattern = r"entityDef\s+(\S+)\s+\{[^\}]+\}"
        entity_names = []
        for entity_def_match in re.finditer(entity_def_pattern, def_file_text):
            self._entity_def_index[entity_def_match.groups()[0]] = entity_def_match.group()
            entity_names.append(entity_def_match.groups()[0])
        return entity_names


    def _get_model_defs(self, def_file_text: str) -> List[str]:
        model_mesh_pattern = r"model\s(\S+)\s\{(?:[^{}]*|\{(?:[^{}]*|\{[^{}]*\})\})*\}"
        model_names = []
        for model_mesh_def_match in re.finditer(model_mesh_pattern, def_file_text):
            try:
                self._model_def_index[model_mesh_def_match.groups()[0]] = EntityArchive._get_mesh_path_from_model_def(model_mesh_def_match.group())
                model_names.append(model_mesh_def_match.groups()[0])
            except MeshMissingError:
                print(f"Missing mesh reference for model def {model_mesh_def_match.groups()[0]}")
        return model_names



class MaterialArchive():
    @staticmethod
    def _get_mat_files(path: str) -> List[str]:
        globs = glob(f"{path}/materials/*.mtr")
        print(f"Found {len(globs)} material files")
        return globs

    def __init__(self, path: str) -> None:
        self._base_path = path
        self._materials_index = {}
        self._mat_files_to_walk = MaterialArchive._get_mat_files(path)

    def search_material_files(material_name: str) -> str:
        pass



class SkinArchive():
    @staticmethod
    def _get_skin_files(path: str) -> List[str]:
        pass


    def __init__(self, path:str) -> None:
        self._base_path = path
        self._skins_index
        self._skin_files_to_walk = SkinArchive._get_skin_files(f"{path}/skins")


    def search_skin_files(skin_name: str) -> str: 
        if skin_name in self._skins_index:
            return self._skins_index[skin_name]

        self._walk_skin_files(skin_name)

        if skin_name in self._skins_index:
            return self._skins_index[skin_name]
        else:
            raise SkinMissingError(f"Couldn't find {skin_name} in {self._base_path}/skins")
                

    def _walk_skin_files(skin_name: str) -> None:
        files_visited = []
        for skin_file in self._skin_files_to_walk:
            with open(skin_file) as skin_file_body:
                skin_defs = self._get_skin_defs(skin_file_body)
                print(f"Found {len(skin_defs)} skin definitons in {skin_file}")
            files_visited.append(skin_file)
            if skin_name in self._skins_index:
                print(f"Found {skin_name} in {skin_file}")
                break
        
        print(f"Indexed {len(files_visited)} skin file(s)")
        self._def_files_to_walk = [f for f in self._def_files_to_walk if f not in files_visited]


if __name__ == "__main__":
    entity_archive = EntityArchive("/home/jeffrey/Downloads/Archive/")
    entity_archive.get_base_path()
    entity_def = entity_archive.search_entity_files("player_base")
    shells_def = entity_archive.search_entity_files("ammo_shells_small")
    model = entity_archive.search_model_def_files("monster_zombie_maint")
    print(entity_def)