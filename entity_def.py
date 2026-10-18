class EntityDef():
    def _find_entity_def_file(entity_name: str) -> str:
        pass

    def _get_entity_def_text(entity_def_path: str) -> str:
        pass

    def _find_head(entity_def_text: str):
        pass

    def _find_skin(entity_def_text: str):
        pass

    def _find_md5_mesh_path():
        pass

    
    def __init__(self, name):
        def_path = _find_entity_def_file(name)
        entity_def_text = _get_entity_def_text(def_path)
        self._name = name
        self._head = _find_head(entity_def_text)
        self._skin = _find_skin(entity_def_text)
        self._md5mesh_path = _find_md5_mesh_path(entity_def_text)

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

class HeadEntityDef():
    def _find_md5mesh(model_text: str):
        pass

    def __init__(self, name, model_text: str):
        self._name = name
        self._md5mesh_path = _find_md5_mesh(model_text)

    def get_name(self) -> str:
        return self._name

    def get_mesh_path(self) -> str:
        return self._md5mesh_path