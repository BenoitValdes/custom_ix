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
        ix.cmds.DisableItems([str(self)], state)
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

class ShadingLayer(SceneItem):
    """
    The Shading Layer is bit unique. Thanks to that class you have easier access to it's content.
    You can add/get/set row data in friendly way.
    """

    def __init__(self, ix_node):
        super(ShadingLayer, self).__init__(ix_node)

        self._default_columns = {"is_active": True, "filter": "", "is_visible": True, "material": "", "clip_map": "", "displacement": "", "shading_variables": ""}

    def add_row(self, is_active=True, filter="", is_visible=True, material="", clip_map="", displacement="", shading_variables=""):
        """Add a row to the shading layer and set the data if they are specified

        Args:
            is_active (bool, optional): Set the state of the is_active column. Defaults to True.
            filter (str, optional): Filter rule that will be used to find the shading group(s) to affect. Defaults to "".
            is_visible (bool, optional): Set the visibility state of the affected shading group(s). Defaults to True.
            material (str, optional): The material that will be applied to the affected shading group(s). Defaults to "".
            clip_map (str, optional): The clip map that will be applied to the affected shading group(s). Defaults to "".
            displacement (str, optional): The displacement node that will be applied to the affected shading group(s). Defaults to "".
            shading_variables (str, optional): The shading variables that could be used by the material given as parametter. Defaults to "".
        """
        row_number = self.get_module().get_rules().get_count()
        ix.cmds.AddShadingLayerRule(str(self), row_number, ["filter", "", "is_visible", "1" if is_visible else "0"])
        self.set_row_values(row_number, is_active, filter, is_visible, material, clip_map, displacement, shading_variables)

    def set_row_values(self, row_number, is_active=True, filter="", is_visible=True, material="", clip_map="", displacement="", shading_variables=""):
        """
        Set values on the row specified.

        Args:
            row_number (int): The row to affect
            is_active (bool, optional): Set the state of the is_active column. Defaults to True.
            filter (str, optional): Filter rule that will be used to find the shading group(s) to affect. Defaults to "".
            is_visible (bool, optional): Set the visibility state of the affected shading group(s). Defaults to True.
            material (str, optional): The material that will be applied to the affected shading group(s). Defaults to "".
            clip_map (str, optional): The clip map that will be applied to the affected shading group(s). Defaults to "".
            displacement (str, optional): The displacement node that will be applied to the affected shading group(s). Defaults to "".
            shading_variables (str, optional): The shading variables that could be used by the material given as parametter. Defaults to "".
        """


        for k, v in locals().items():
            if k in self._default_columns and self._default_columns[k] != v:
                if isinstance(v, bool):
                    v = "1" if v else "0"
                if not isinstance(v, list):
                    v = [v]
                ix.cmds.SetShadingLayerRulesProperty(str(self), [int(row_number)], str(k), [str(value) for value in v])

    def get_all_rows(self):
        result = []
        for i in range(self.get_module().get_rules().get_count()):
            result.append(self.get_row(i))

        return result


    def get_row(self, row_number):
        """
        Get all the columns data for the row specified as parameter

        Args:
            row_number (int): The row to affect

        Returns:
            ShadingLayerRow: A simple OOP object that will allow you to get the column data for this row
        """
        if not row_number in range(self.get_module().get_rules().get_count()):
            ix.log_warning("The row `{}` can't be found in `{}`".format(row_number, self))
            return None
        result = ShadingLayerRow(self, row_number)
        for k in self._default_columns:
            setattr(result, k, self.get_module().get_rule_value(row_number, k))
        return result

class ShadingLayerRow(object):
    """
    Simple Class that represent a Shading Layer row. Created only to give an OOP access to the user.
    """
    def __init__(self, sl, row_number):
        self._sl = sl
        self.row_number = row_number
        self.is_active = None
        self.filter = None
        self.is_visible = None
        self.material = None
        self.clip_map = None
        self.displacement = None
        self.shading_variables = None

    def get_shading_layer(self):
        return self._sl

    def __repr__(self):
        result = {}
        for attr in ["is_active", "filter", "is_visible", "material", "clip_map", "displacement", "shading_variables"]:
            result[attr] = getattr(self, attr)

        return str(result)

    