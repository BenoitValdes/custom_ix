import wrapper
reload(wrapper)
import attribute_class
reload(attribute_class)


class SceneItem(wrapper.Wrapper):
    """
    This Class wrap Clarisse items one to be OOP friendly.
    To avoid any conflict with Clarisse item's attributes, all the function had to have a prefix.
    ex: is, get, set, add

    If the module is in debug mode (__builtins__["cix_is_debug"]=True) a test function will be
    executed at the end of the init.
    """

    def __init__(self, ix_node):
        super(SceneItem, self).__init__(ix_node)
        self._attr_list = []

        # Add all item's attributes as class properties
        for i in range(self._node.get_attribute_count()):
            attr = attribute_class.Attribute(self._node.get_attribute(i))
            self._attr_list.append(attr)
            setattr(self, attr.get_name(), attr)

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
        result = super(SceneItem, self).__dir__()
        result += [attr.get_name() for attr in self._attr_list]
    
        return result