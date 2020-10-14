"""
DISCLAIMER: This repository and it's development is not linked to ISOTROPIX in any manear.

@Author: Benoit Valdes
"""
from ix import *

class Item:
    """
    This Class wrap Clarisse items one to be OOP friendly.
    To avoid any conflict with Clarisse item's attributes, all the function had to have a prefix.
    ex: is, get, set, add

    If the module is in debug mode (__builtins__["cix_is_debug"]=True) a test function will be
    executed at the end of the init.
    """

    def __init__(self, ix_item):
        self._item = ix.get_item(str(ix_item))
        self._attr_list = []

        self._avoid_ix_item_methods = []
        self._avoid_self_methonds = ["_is_callable", "_test_override_functions"]

        # Add all item's attributes as class properties
        for i in range(self._item.get_attribute_count()):
            attr = Attribute(self._item.get_attribute(i))
            self._attr_list.append(attr)
            setattr(self, attr.get_name(), attr)

        if __builtins__.get("cix_is_debug") is True:
            self._test_override_functions()

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

    def get_ix_item(self):
        """
        Get the Clarisse item used in this Class

        Returns:
            OfItem: The Clarisse item that represent this class
        """
        return self._item

    def _is_callable(self, attr):
        """
        Determine if the attr name as argument is callable.
        This function is a helper to know if self._item has the attr in it's dir
        and if it's a method

        Args:
            attr (str): Attr name we want to check

        Returns:
            bool: True if the attr is callable and False if it doesn't pass the condition
        """
        if attr not in self._avoid_ix_item_methods and hasattr(self._item, attr) and callable(getattr(self._item, attr)):
            return True
        return False
        
    def _test_override_functions(self):
        """
        Test if the curren methods do not override a method of Clarisse's item.
        It can be wanted so it's just a print, nothing blocking.
        """
        print("`_test_override_functions` needs to be implemented")
    
    def __getattr__(self, attr):
        """
        That class used to be called when a class attribute is not found.
        As we wrap a Clarisse item, lot of functions works as is and don't need to be written again.
        Before raise an error, we first check if the function exists in Clarisse's item.

        Args:
            attr (str): The name of the attribute which is not found.

        Raises:
            AttributeError: If the attribute is not even found in Clarisse item or don't pass the condition.

        Returns:
            [unknown]: The result of the function found in Clarisse's item.
        """
        if self._is_callable(attr):
            def wrapper(*args, **kwargs):
                return getattr(self._item, attr)(*args, **kwargs)
            return wrapper
        raise AttributeError("{} instance has no attribute `{}`".format(self.__class__.__name__, attr))
        
    def __dir__(self):
        """
        Override the dir function to have something coherent when we use dir() (needed because of __getattr__ override)
        It should return a list of:
            - The class attributes (what should return a classic dir())
            - Clarisse's item attributes (as we add them dinamicaly to be OOP friendly)
            - A parsed dir() of the Clarisse item (remove everything which is not a function or already present)


        Returns:
            list[str]: The list of all the attributes availlable of this Class
        """
        result = dir(self.__class__)

        # hide methods internal methods when user call dir()
        for method in self._avoid_self_methonds:
            if method in result:
                result.remove(method)

        result += [attr.get_name() for attr in self._attr_list]

        for attr in dir(self._item):
            if not attr.startswith("_") and self._is_callable(attr) and not attr in result:
                result.append(attr)
    
        return result

    def __repr__(self):
        """
        Override the representation of this Class to mimic Clarisse's one

        Returns:
            str: Clarisse item path
        """
        return str(self._item)

class Attribute:
    def __init__(self, ix_attr):
        self._attr = ix.get_item(str(ix_attr))

    def get_value(self):
        ix.log_warning("Attribute `{}` of type `{}` and typename `{}`".format(self.get_name(), self.get_type(), self.get_type_name()))
        result = []
        function_to_use = None
        if self.get_type() is 1:
            function_to_use = self.get_bool
        elif self.get_type() is 2:
            function_to_use = self.get_long
        elif self.get_type() is 3:
            function_to_use = self.get_double
        elif self.get_type() is 4:
            function_to_use = self.get_string
        elif self.get_type() is 5:
            function_to_use = self.get_object
        # elif self.get_type() is 6:
        #     pass
        else:
            ix.log_warning("`cix` module do not handle get_value() on attribute of type `{}`.".format(self.get_type()))

        if function_to_use is not None:
            if self.get_value_count() > 1:
                for i in range(self.get_value_count())
                    self.result.append(function_to_use(i))
            else:
                self.result.append(function_to_use())

        if len(result) is 0:
            return None
        elif len(result) is 1:
            return result[0]
        else:
            return result

    def set_value(self, value):
        pass
    
    def get_type_name(self):
        return self._item.get_type_name(self.get_type())

    def __repr__(self):
        """
        Override the representation of this Class to mimic Clarisse's one

        Returns:
            str: Clarisse attribute path
        """
        return str(self._attr)

def get_item(path):
    """Create an Item Class from the path argument.

    Args:
        path (str|OfItem): Clarisse Item or it's path as string

    Returns:
        Item: The wrapped item of the give path
    """
    return Item(path)
