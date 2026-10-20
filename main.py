from pathlib import Path
from sys import exit, argv
from copy import deepcopy

from entity_def import EntityDef
from md5mesh import Md5mesh
from material import Material, MaterialFragment
from skin import Skin
from game_files import EntityArchive, MaterialArchive, SkinArchive, MeshMissingError, SkinMissingError

# argv[1]: File containing list of entity names for which to create new materials and skins
# argv[2]: Path to text file containing the material content to append to the existing material copies
# argv[3]: Path of base folder where entities/materials/skins etc live
# argv[4]: Path of materials file to write to. Will be created or appended if exists
# argv[5]: Path of skins file to write to. Will be created or appended if exists
# argv[6]: Material/skin suffix - appended to exisiting material/skin names to uniquely identify the new materials/skins for the entity

def is_valid_base_folder(base_path: str) -> bool:
    if not Path(f"{base_path}/def").exists:
        return False
    if not Path(f"{base_path}/materials").exists:
        return False
    if not Path(f"{base_path}/skins"):
        return False
    if not Path(f"{base_path}/models/md5").exists:
        return False
    return True

def get_file_text(path: str) -> str:
    with open(path) as file_body:
        return "\n".join(map(str.strip, file_body.readlines()))


if __name__ == "__main__":
    # parse entity names list and material fragment
    try:
        if not Path(argv[1]).exists:
            raise FileNotFoundError(f"File '{argv[2]}' containing material fragment to append doesn't exist")
        if not Path(argv[2]).exists:
            raise FileNotFoundError(f"Entity list file '{argv[1]}' doesn't exist")
        if not Path(argv[3]).exists:
            raise FileNotFoundError(f"Doom 3 Base folder '{argv[3]}' doesn't exist")
        if not is_valid_base_folder(argv[3]):
            raise IOError(f"{argv[3]} isn't a valid base folder. Missing one or more of the following: def, materials, skins, models")
    except Exception as error:
        print("usage: python main.py <entities_file> <material_file> <base_path> <materials_output> <skins_output>")
        print(error)
        exit()

    material_fragment = MaterialFragment(get_file_text(argv[2]))

    with open(argv[1]) as entity_list:
        entity_archive = EntityArchive(argv[3])
        # init entities list
        entities = []
        for line in entity_list.read().splitlines():
            entity = EntityDef(line, entity_archive)
            entities.append(entity)
            print(f"Parsed entity {line}")
            # Add head entity to be skinned if applicable
            if (entity.has_head()):
                head = entity.get_head()
                entities.append(head)
                print(f"Parsed {head.get_name()} for {line}")

    # for each entity (and head entity)
    material_archive = MaterialArchive(argv[3])
    skin_archive = SkinArchive(argv[3])
    materials_created = set()                   # Avoid redefining custom materials
    skins_created = set()                       # Head skins can be repeated
    for entity in entities:
        # Find all the materials in the md5mesh file
        try:
            mesh = Md5mesh(f"{argv[3]}/{entity.get_mesh_path()}", material_archive)
        except FileNotFoundError:
            print(f"Mesh file doesn't exist for {entity.get_name()}. Skipping")
            continue
        except MeshMissingError:
            print(f"Mesh not defined in the inheritance hierarchy for {entity.get_name()}")
            continue
        print(f"Found mesh {entity.get_mesh_path()} for {entity.get_name()}")
        materials = mesh.get_materials()
        print(f"Found {len(materials)} materials in {entity.get_mesh_path()}")
        material_mapping = {}
        if entity.has_skin():
            try:
                current_skin = Skin(entity.get_skin_name(), None, skin_archive)
            except SkinMissingError as e:
                print(e)
                continue
        else:
            current_skin = None
        for source_material in materials:
            # If the material is skinned as a basic texture i.e. texture/common/nodraw, texture/common/shadow etc.
            if current_skin and current_skin.material_overridden_with_common_texture(source_material.get_name()):
                # Pass the common mapping through into the new skin
                material_mapping[source_material.get_name()] = current_skin.get_overriden_material(source_material.get_name())
            else:
                # Create override material and add new shader fragment code
                override_material = deepcopy(source_material)
                # Update material name
                override_material.set_name(f"{source_material.get_name()}_{argv[6]}")
                # Add fragment to material object
                override_material.composite_materials(material_fragment)
                print(f"Adding fragment to {override_material.get_name()}")
                if override_material.get_name() not in materials_created:
                    # serialize to new material file (append if necessary)
                    override_material.serialize_copy(argv[4], argv[6])
                    print(f"Serialized {override_material.get_name()} to {argv[4]}")
                    materials_created.add(override_material.get_name())
                else:
                    print(f"Material {override_material.get_name()} already created. Skipping serialization")
                material_mapping[source_material.get_name()] = override_material.get_name()
        # Create new skin, reference existing material with the new material copy
        override_skin = Skin(f"skins/{entity.get_name()}_{argv[6]}", material_mapping)
        if override_skin.get_name() not in skins_created:
            # Serialize skin to output file
            override_skin.serialize_copy(argv[5])
            print(f"Serialized {override_skin.get_name()} to {argv[5]}")
            skins_created.add(override_skin.get_name())
        else:
            print(f"Skin {override_skin.get_name()} already created. Skipping serialization")