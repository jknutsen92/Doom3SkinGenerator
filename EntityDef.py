class EntityDef():
    def __init__(self, name):
        def_path = _find_entity_def_file(name)
        self._name = name
        self._entity_def_text = _get_entity_def_text(def_path)
        self._head = _find_head()
        self._skin = _find_skin()
        self._md5mesh = None

    def _get_md5model_text(path: str):
        pass

    def _find_entity_def_file(entity_name: str):
        pass

    def _get_entity_def_text(entity_def_path: str):
        pass

    def _find_head(entity_def_text):
        pass

    def _find_skin(entity_def_text: str):
        pass

class HeadModel():
    def __init__(self, model_text: str):
        pass
