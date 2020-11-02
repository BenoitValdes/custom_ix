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
        Get all the attributes of the current item as a list

        Returns:
            list[Attribute]: The list of the ix_node attributes
        """
        return [cix.get_item(self.get_attribute(i)) for i in range(self.get_attribute_count())]

    def __getattr__(self, attr):
        """
        Override Wrapper's class __getattr__ method to allow the user to get clarisse node attribute (like translate, resolution...)
        directly as a class attribute.
        That allow to have a dynamic way to get an attribute.

        Args:
            attr (str): The name of the attribute which is not found.

        Returns:
            [unknown]: Clarisse attribute or Wrapper's return
        """
        if hasattr(self.get_ix_node(), "attribute_exists"):
            result = self.get_ix_node().attribute_exists(attr)
            if result is not None:
                return cix.get_item(result, silent=True)

        return super(ProjectItem, self).__getattr__(attr)       

    def __dir__(self):
        """
        Override the dir function to add  Clarisse's item attributes (as we add them dinamicaly to be OOP friendly)

        Returns:
            list[str]: The list of all the attributes availlable of this Class
        """
        result = super(ProjectItem, self).__dir__()
        result += [attr.get_name() for attr in self.get_attribute_list()]
    
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

    def add_custom_attribute(self, attr_name, kindof, group_name, array_length=1, num_range=None, ui_range=None, texturable=False, animatable=False, shading_var=False, allow_expression=False):
        """
        Add a custom attribute to the current item.

        Args:
            attr_name (str): name of the future attributes
            kindof (str): Kindof attribute you want to create (long, double, bool, string, rgba...)
            group_name (str): Name of the group that will live the new attr (Kinematics, visibility...)
            array_length (int, optional): If the attribute has be be an array type (Like translate or resolution) set the array size here. Defaults to 1.
            num_range (list[int], optional): Give a min/max range of the attribute. Defaults to None.
            ui_range (list[int], optional): Give a min/max range of the UI in the attr editor. Defaults to None.
            texturable (bool, optional): Allow the attr to be texturable. Defaults to False.
            animatable (bool, optional): Allow the attr to be animatable. Defaults to False.
            shading_var (bool, optional): Allow the attr to be shading_var. Defaults to False.
            allow_expression (bool, optional): Allow the attr to be texturable (Due to a clarisse,s bug it's all the time True). Defaults to False.

        Returns:
            None|Attribute: If the attribute can't be created for what ever reason it returns None else it return an Attribute instance.
        """
        if self.attribute_exists(attr_name):
            ix.log_warning("An attribute with the same name already exists.")
            return None

        mapping_name_vhint = {
            "angle": {"vhint": "VISUAL_HINT_ANGLE", "kindof": 2},
            "area": {"vhint": "VISUAL_HINT_AREA", "kindof": 2},
            "bool": {"vhint": "VISUAL_HINT_DEFAULT", "kindof": 0},
            "color": {"vhint": "VISUAL_HINT_COLOR", "kindof": 2},
            "curve": {"vhint": "VISUAL_HINT_DEFAULT", "kindof": 7},
            "distance": {"vhint": "VISUAL_HINT_DISTANCE", "kindof": 2},
            "double": {"vhint": "VISUAL_HINT_DEFAULT", "kindof": 2},
            "file": {"vhint": "VISUAL_HINT_DEFAULT", "kindof": 4},
            "filename_open": {"vhint": "VISUAL_HINT_FILENAME_OPEN", "kindof": 3},
            "filename_save": {"vhint": "VISUAL_HINT_FILENAME_SAVE", "kindof": 3},
            "folder": {"vhint": "VISUAL_HINT_FOLDER", "kindof": 3},
            "frame": {"vhint": "VISUAL_HINT_FRAME", "kindof": 1},
            "frequency": {"vhint": "VISUAL_HINT_FREQUENCY", "kindof": 2},
            "gradient": {"vhint": "VISUAL_HINT_GRADIENT", "kindof": 7},
            "l": {"vhint": "VISUAL_HINT_L", "kindof": 2},
            "la": {"vhint": "VISUAL_HINT_LA", "kindof": 2},
            "long": {"vhint": "VISUAL_HINT_DEFAULT", "kindof": 1},
            "memsize": {"vhint": "VISUAL_HINT_MEMSIZE", "kindof": 2},
            "multiline": {"vhint": "VISUAL_HINT_MULTILINE", "kindof": 2},
            "percentage": {"vhint": "VISUAL_HINT_PERCENTAGE", "kindof": 2},
            "pixel": {"vhint": "VISUAL_HINT_PIXEL", "kindof": 1},
            "rgb": {"vhint": "VISUAL_HINT_RGB", "kindof": 2},
            "rgba": {"vhint": "VISUAL_HINT_RGBA", "kindof": 2},
            "sample": {"vhint": "VISUAL_HINT_SAMPLE", "kindof": 1},
            "sample_per_pixel": {"vhint": "VISUAL_HINT_SAMPLE_PER_PIXEL", "kindof": 1},
            "scale": {"vhint": "VISUAL_HINT_SCALE", "kindof": 2},
            "script": {"vhint": "VISUAL_HINT_SCRIPT", "kindof": 3},
            "second": {"vhint": "VISUAL_HINT_SECOND", "kindof": 2},
            "string": {"vhint": "VISUAL_HINT_DEFAULT", "kindof": 3},
            "subframe": {"vhint": "VISUAL_HINT_SUBFRAME", "kindof": 2},
            "subpixel": {"vhint": "VISUAL_HINT_SUBPIXEL", "kindof": 2},
            "subsample": {"vhint": "VISUAL_HINT_SUBSAMPLE", "kindof": 2},
            "time": {"vhint": "VISUAL_HINT_TIME", "kindof": 2},
            "watt": {"vhint": "VISUAL_HINT_WATT", "kindof": 2},
        }

        presets = {
            "color": {"array_length": 3},            
            "la": {"array_length": 2},      
            "rgb": {"array_length": 3},   
            "rgba": {"array_length": 4},
        }
        
        if not kindof in mapping_name_vhint.keys():
            ix.log_warning("There is not type `{}`. You can pick one of the following ones:\n{}".format(kindof, mapping_name_vhint))

        if kindof in presets:
            for var, value in presets[kindof].items():                
                if var == "array_length":
                    array_length = value

        container = "CONTAINER_ARRAY" if array_length > 1 else "CONTAINER_SINGLE"

        result_mapping = {
            "container": container,
            "vhint": mapping_name_vhint[kindof]["vhint"],
            "group": group_name,
            "count": array_length,
            "num_min": None if not num_range else num_range[0],
            "num_max": None if not num_range else num_range[1],
            "ui_min": None if not ui_range else ui_range[0],
            "ui_max": None if not ui_range else ui_range[1],
            "texturable": texturable,
            "animatable": animatable,
            "shading_var": shading_var,
            "allow_expression": allow_expression,
        }

        headers = []
        values = []
        for header, value in result_mapping.items():
            if value:
                headers.append(header)
                values.append(str(value))

        ix.cmds.CreateCustomAttribute(  
            [str(self.get_ix_node())],
            attr_name,
            mapping_name_vhint[kindof]["kindof"],
            headers,
            values
        )

        return self.get_attribute(attr_name)

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

    def set_values(self, **kwargs):
        self.get_shading_layer().set_row_values(self.row_number, **kwargs)

    def __repr__(self):
        result = {}
        for attr in ["is_active", "filter", "is_visible", "material", "clip_map", "displacement", "shading_variables"]:
            result[attr] = getattr(self, attr)

        return str(result)

    