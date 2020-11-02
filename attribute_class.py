import ix, wrapper
reload(wrapper)

class Attribute(wrapper.Wrapper):
    def __init__(self, ix_node):
        super(Attribute, self).__init__(ix_node)
        self._node = ix.get_item(str(ix_node))

    def get_values(self, disabled=False):
        """
        Get the value of the current attribute.
        Not matter the type of attribute.

        Args:
            disabled (bool, optional): If True return the disabled objects. Defaults to False.

        Returns:
            bool|int|float|str|list: Return the value of the attribute (if the attribute is an array, return a list)
        """
        ix.log_warning("Attribute `{}` of type `{}` and typename `{}`".format(self.get_name(), self.get_type(), self.get_type_name()))
        result = []
        function_to_use = None
        if self.get_type() is 0:
            function_to_use = self.get_bool
        elif self.get_type() is 1:
            function_to_use = self.get_long
        elif self.get_type() is 2:
            function_to_use = self.get_double
        elif self.get_type() is 3:
            function_to_use = self.get_string
        elif self.get_type() in [5, 6]:
            function_to_use = self.get_object
        else:
            ix.log_warning("`cix` module do not handle get_values() on attribute of type `{}`.".format(self.get_type()))

        if function_to_use is not None:
            if self.get_value_count() > 1:
                for i in range(self.get_value_count()):
                    result.append(function_to_use(i))
            else:
                result.append(function_to_use())

        if len(result) is 0:
            return None
        elif len(result) is 1:
            return result[0]
        else:
            return result

    def set_values(self, values):
        """
        Set the value given as paremeter on the current attribute by using ix.cmds.SetValues().

        Args:
            values (bool|int|float|str|list): The value we want to set. That can be a string, a int, a float or a list of all of these.
        """
        # as ix.cmds.SetValues() needs a list of string to set the value, we've to be sure `value` is a list
        if not isinstance(values, (list, tuple)):
            values = [values]

        ix.cmds.SetValues([str(self)], [str(v) for v in values])

    def set_texture(self, texture_node):
        ix.cmds.SetTexture([str(self)], str(texture_node))

    def add_values(self, values):
        """
        Use ix.cmds.SetValues() on self with values given as parametter

        Args:
            values (str|list[str]: [description]
        """
        if not isinstance(values, (list, tuple)):
            values = [values]

        ix.cmds.AddValues([str(self)], [str(v) for v in values])
    
    def get_type_name(self):
        """
        Return the type_name without having to specify the current type.

        Returns:
            str: THe type name of the current attribute
        """
        return self._node.get_type_name(self.get_type())