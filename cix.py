"""
DISCLAIMER: This repository and it's development is not linked to ISOTROPIX in any manear.

This module is meant to wrap Clarisse API in a way it's easier for a user used to python or other DCC API like Maya to work with Clarisse API.
CIX means Custom IX. There is almost no override of IX API, it's just a different way to access and manipulate Clarisse Items.
The bigest part is to deal with Clarisse Nodes and allow fast access to attributes, get the connections between nodes or even access to rows of shading layers in an
elegant python way.

Clarisse original API is a bit hard to work with at the begining but is very powerfull because it allow the user to do amlmost everything than C++ can do.
This is the reason why this wrapper override a few thing of the original API and allow you to get back the the original API whenever you need to.

You can work with original Clarisse API and then pass Clarisse items to CIX API if you need easy to use functions or method to do something faster than what IX allow to do.

@Author: Benoit Valdes
"""
import ix
from ix import *
import items_class
reload(items_class)

def get_item(path, silent=False):
    """Create an Item Class from the path argument.

    Args:
        path (str|OfItem): Clarisse Item or it's path as string
        silent (bool): Tf True, test if the item is an item and avoid any log print

    Returns:
        Wrapper: The wrapped item of the give path
    """
    map_dict = {
        "Attribute": items_class.attribute_class.Attribute,
        "Context": items_class.Context,
        "SceneItem": items_class.SceneItem,
        "ShadingLayer": items_class.ShadingLayer,
    }
    ix_node = ix.item_exists(str(path))
    if ix_node is None:
        if silent is True:
            return path
        else:
            ix.log_warning("`{}` is not a valid Clarisse item and/or can't be found".format(path))
            return None

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

def create_item(name, class_name, parent_ctx=get_current_context()):
    """
    Create a Clarisse item and return a wrapper Class.
    You can also create a context through this function by giving the class_name Context.
    It can help to automate script and don't have to do if/else.

    Args:
        name (str): Name of the item we want to create
        class_name (str): Clarisse Class Name of the item
        parent_ctx (Context|str, optional): The context where the item will be created.
                                            Defaults to get_current_context().

    Returns:
        Wrapper: The wrapped created item
    """
    if class_name == "Context":
        return create_context(name, parent_ctx)
    parent_ctx = get_item(parent_ctx)
    item = ix.create_object(name, class_name, parent_ctx.get_ix_node())
    if item:
        return get_item(item)
    else:
        return None

def create_context(name, parent_ctx=get_current_context()):
    """
    Create a Clarisse context.

    Args:
        name (str): Name of the context we want to create
        parent_ctx (Context|str, optional): The context where the item will be created.
                                            Defaults to get_current_context().

    Returns:
        Wrapper: The wrapped created context
    """
    item = ix.cmds.CreateContext(name, str(parent_ctx))
    if item:
        return get_item(item)
    else:
        return None