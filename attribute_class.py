import ix, wrapper
reload(wrapper)

class Attribute(wrapper.Wrapper):
    def __init__(self, ix_node):
        super(Attribute, self).__init__(ix_node)
        self._node = ix.get_item(str(ix_node))

    def get_value(self):
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
            ix.log_warning("`cix` module do not handle get_value() on attribute of type `{}`.".format(self.get_type()))

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

    def set_value(self, value):
        pass
    
    def get_type_name(self):
        return self._node.get_type_name(self.get_type())