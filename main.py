from pathlib import Path
from sys import exit, argv

from entity_def import EntityDef
from md5mesh import Md5mesh
from material import Material
from skin import Skin

# argv[1]: File containing list of entitie names for which to create new materials and skins
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

    material_fragment = Material.parse_material_fragment(argv[2])

    with open(argv[1]) as entity_list:
        # init entities list
        entities = []
        for line in entity_list.readlines():
            try:
                entity = EntityDef(line)
                entities.append(entity)
                print(f"Parsed entity {line}")
                # Add head entity to be skinned if applicable
                if (entity.has_head()):
                    head = entity.get_head()
                    entities.append(head)
                    print(f"Parsed {head.get_name()} for {line}")
            except Exception:
                print(f"Invalid entity {line} - skipping")
                continue

    # for each entity (and head entity)
    for entity in entities:
        # Find all the materials in the md5mesh file
        mesh = Md5mesh(entity.get_mesh_path(), argv[6])
        print(f"Found mesh {entity.get_mesh_path()} for {entity.get_name()}")
        materials = mesh.get_materials()
        print(f"Found {len(materials)} materials in {entity.get_mesh_path()}")
        for material in materials:
            # Add fragment to material object
            material.append_material_fragment(argv[2])
            print(f"Adding fragment to {material.get_base_name()}")
            # serialize to new material file (append if necessary)
            material.serialize_copy(argv[4])
            print(f"Serialized {material.get_modified_name()} to {argv[4]}")

        # Create new skin, reference existing material with the new material copy
        skin = Skin(f"skins/{entity.get_name()}_{argv[6]}", materials)

        # Serialize skin to output file
        skin.serialize_copy(argv[5])
        print(f"Serialized {skin.get_name()} to {argv[5]}")
