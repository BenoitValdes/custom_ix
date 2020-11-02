import ix
import cix

class Wrapper(object):
    """
    This class is used to act as a wrapper. Lot of Clarisse object method are working perfectly as is.
    So instead of rewritting them and maintain them each time they changed or new one are added.
    the easiest way is to allow the user to acces to the ix node class directly through that one.

    It is good also to have more control on it by beeing able to hide methods and attributes.
    All the attributes have to be hidden to avoid any confusion. And we can also hide some methods.
    By default all the overriden methods make the original one hiden.
    
    It's goal is to have an OOP friendly way to access to an item|attribute withing Clarisse.

    The node can be an Item or an Attribute, it doesn't matter.
    """

    def __init__(self, ix_node):
        self._node = ix.get_item(str(ix_node))
        self._avoid_ix_node_methods = []
        self._avoid_self_methods = ["_is_callable", "_test_override_functions"]
        if __builtins__.get("cix_is_debug") is True:
            self._test_override_functions()

    def get_ix_node(self):
        """
        Get the Clarisse node used in this Class

        Returns:
            OfItem|OfAttr: The Clarisse node that represent this class
        """
        return self._node

    def _is_callable(self, method):
        """
        Check if the method we are trying to call from self._node can be called.
        As we can tell that some methods form self._node can be avoided

        Args:
            method (str): Method name we want to use

        Returns:
            bool: True if the method is callable and False if it doesn't pass the condition
        """
        if method not in self._avoid_ix_node_methods and hasattr(self._node, method) and callable(getattr(self._node, method)):
            return True
        return False
        
    def _test_override_functions(self):
        """
        Test if the curren methods do not override a method of Clarisse's node.
        It can be wanted so it's just a print, nothing blocking.
        """
        print("`_test_override_functions` needs to be implemented")
    
    def __getattr__(self, attr):
        """
        That class used to be called when a class attribute is not found.
        As we wrap a Clarisse node, lot of functions works as is and don't need to be written again.
        Return the cix.get_item() result of the function. If the result is an item, it will be wrapped automatically
        Else it will return what should be returned.
        Before raise an error, we first check if the function exists in Clarisse's node.

        Args:
            attr (str): The name of the attribute which is not found.

        Raises:
            AttributeError: If the attribute is not even found in Clarisse node or don't pass the condition.

        Returns:
            [unknown]: The result of the function found in Clarisse's node.
        """
        if self._is_callable(attr):
            def wrapper(*args, **kwargs):
                return cix.get_item(getattr(self.get_ix_node(), attr)(*args, **kwargs), silent=True)
            return wrapper
        raise AttributeError("{} instance has no attribute `{}`".format(self.__class__.__name__, attr))
        
    def __dir__(self):
        """
        Override the dir function to have something coherent when we use dir() (needed because of __getattr__ override)
        It should return a list of:
            - The class attributes (what should return a classic dir())
            - A parsed dir() of the Clarisse node (remove everything which is not a function or already present)


        Returns:
            list[str]: The list of all the attributes availlable of this Class
        """
        result = dir(self.__class__)

        # hide methods internal methods when user call dir()
        for method in self._avoid_self_methods:
            if method in result:
                result.remove(method)

        for method in dir(self._node):
            if not method.startswith("_") and self._is_callable(method) and not method in result:
                result.append(method)
    
        return result

    def __repr__(self):
        """
        Override the representation of this Class to mimic Clarisse's one

        Returns:
            str: Clarisse node path
        """
        return str(self._node)