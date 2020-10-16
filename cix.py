"""
DISCLAIMER: This repository and it's development is not linked to ISOTROPIX in any manear.

@Author: Benoit Valdes
"""
import ix
from ix import *
import items_class
reload(items_class)

def get_item(path):
    """Create an Item Class from the path argument.

    Args:
        path (str|OfItem): Clarisse Item or it's path as string

    Returns:
        Item: The wrapped item of the give path
    """
    map_dict = {
        "Attribute": items_class.attribute_class.Attribute,
        "SceneItem": items_class.SceneItem,
        "Context": items_class.Context,
    }
    
    ix_node = ix.get_item(str(path))
    
    if "get_type" in  dir(ix_node):
        kindof = "Attribute"
    elif ix_node.is_context() is True:
        kindof = "Context"
    else:
        kindof = ix_node.get_class_name()
        if not kindof in map_dict:
            kindof = "SceneItem"

    # TODO: Check the kindof item it is an return the right Wrapper Class
    return map_dict[kindof](ix_node)

def get_current_context():
    return get_item(ix.get_current_context())
