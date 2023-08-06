class NodeType:
    """
    Модель типа узла
    """

    class NodeTypeProperty:
        """
        Модель для свойства типа
        """

        def __init__(self, name, default_value, position, **other):
            """
            # todo тут далеко не все атрибуты свойства типа
            :param node_type_property_body:
            """
            self.name = name
            self.position = position
            self.default_value = default_value

        def __str__(self):
            return f"{self.name}: {self.default_value}"

    def __init__(self, id, name, displayable, default_child_node_type_id, icon, properties, **other):
        self.id = id
        self.name = name

        self.displayable = displayable
        self.default_child_node_type_id = default_child_node_type_id
        self.icon = icon
        self.properties = [NodeType.NodeTypeProperty(**t) for t in properties]

    def __repr__(self):
        return f"NodeType('{self.id}', '{self.name}', ...)"
