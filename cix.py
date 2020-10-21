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
        "Context": items_class.Context,
        "SceneItem": items_class.SceneItem,
        "ShadingLayer": items_class.ShadingLayer,
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
    """override of ix.get_current_context() to return wrapped class

    Returns:
        Context: the current context your are in Clarisse
    """
    return get_item(ix.get_current_context())

def reference_file(path, parent_ctx=get_current_context()):
    """
    override of ix.reference_file() to return wrapped class

    Args:
        path (str): path of the file to be referenced
        parent_ctx (Context|str, optional): The parent context you want to reference your file.
                                            Defaults to get_current_context().

    Returns:
        Context: The referenced context
    """
    parent_ctx = get_item(parent_ctx)
    ref_ctx = ix.reference_file(parent_ctx.get_ix_node(), path)

    return get_item(ref_ctx)
