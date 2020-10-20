import ix
import cix
import wrapper
reload(wrapper)
import attribute_class
reload(attribute_class)


class ProjectItem(wrapper.Wrapper):
    """
    This Class wrap Clarisse items one to be OOP friendly.
    To avoid any conflict with Clarisse item's attributes, all the function had to have a prefix.
    ex: is, get, set, add

    If the module is in debug mode (__builtins__["cix_is_debug"]=True) a test function will be
    executed at the end of the init.
    """

    def __init__(self, ix_node):
        super(ProjectItem, self).__init__(ix_node)
        self._attr_list = []

        # Add all item's attributes as class properties
        for i in range(self._node.get_attribute_count()):
            attr = attribute_class.Attribute(self._node.get_attribute(i))
            self._attr_list.append(attr)
            setattr(self, attr.get_name(), attr)

    def set_disabled(self, state=True):
        """
        Disable the node

        Args:
            state (bool, optional): The state of the node we want at the end. If False, the node will be enabled.
                                    Defaults to True.

        Returns:
            ProjectItem: The current node
        """
        ix.cmds.DisabledItems([str(self)], state)
        return self

    def get_attribute_list(self):
        """
        Get all the attributes of the current item as a lit

        Returns:
            list[Attribute]: The list of the attributes (not Clarisse attributes but `cix` ones)
        """
        return self._attr_list        

       
    def __dir__(self):
        """
        Override the dir function to add  Clarisse's item attributes (as we add them dinamicaly to be OOP friendly)

        Returns:
            list[str]: The list of all the attributes availlable of this Class
        """
        result = super(ProjectItem, self).__dir__()
        result += [attr.get_name() for attr in self._attr_list]
    
        return result
        
class SceneItem(ProjectItem):
    """
    This Class wrap Clarisse items one to be OOP friendly.
    To avoid any conflict with Clarisse item's attributes, all the function had to have a prefix.
    ex: is, get, set, add

    If the module is in debug mode (__builtins__["cix_is_debug"]=True) a test function will be
    executed at the end of the init.
    """

    def __init__(self, ix_node):
        super(SceneItem, self).__init__(ix_node)

    def add_custom_attribute(self, group_name, attr_name, kindof, array_length=1):
        """
        Add a custom attribute to the item.

        Args:
            group_name (str): Group name in the Attribute Editor (created if it doesn't exists)
            attr_name (str): Name of the attribute
            kindof (str): Type of attribute (string, filename, double, bool...)
            array_length (int, optional): For some attribute type (double, long...) you can specify an array to
                                          represent your attribute. Defaults to 1.

        Raises:
            AttributeError: It's not implemented yet so it raise an error because you can't use it.
        """
        raise AttributeError("Need to be implemented")

class Context(ProjectItem):
    """
    This Class wrap Clarisse items one to be OOP friendly.
    To avoid any conflict with Clarisse item's attributes, all the function had to have a prefix.
    ex: is, get, set, add

    If the module is in debug mode (__builtins__["cix_is_debug"]=True) a test function will be
    executed at the end of the init.
    """

    def __init__(self, ix_node):
        super(Context, self).__init__(ix_node)

    def get_children(self, ctx_only=False, items_only=False, recursive=False):
        """
        TODO: add param filter: allow to get the list filtered by classname (could solve time to find a specific item)
        Get the childrens of the context.

        Args:
            ctx_only (bool, optional): If True, only return contexts (not compatible with `items_only`). Defaults to False.
            items_only (bool, optional): If True, return everything else than context (not compatible with `ctx_only`). Defaults to False.
            recursive (bool, optional): If True, go through the sub contexts. Defaults to False.

        Returns:
            [type]: [description]
        """
        result = []
        objects = ix.api.OfItemVector()
        function = None
        if recursive:
            function = self._node.get_all_items
        else:
            function = self._node.get_items

        function(objects)

        for i in range(objects.get_count()):
            item = objects[i]

            if item.is_context() is True and (ctx_only is True or items_only is False):
                result.append(cix.get_item(item))

            elif item.is_context() is not True and (ctx_only is False or items_only is True):
                result.append(cix.get_item(item))

        return result