class HTMLNode:
    def __init__(
        self, tag=None, value=None, children=None, props=None, self_closing=False
    ):
        if not (tag or value):
            raise ValueError("Either tag or value must be provided")

        if self_closing and (children or not tag):
            raise ValueError("Self-closing nodes must have a tag and no children")

        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}
        self.self_closing = self_closing

    def __repr__(self):
        args = f"{self.tag!r}, {self.value!r}, {self.children!r}, {self.props!r}, {self.self_closing}"
        return f"{self.__class__.__name__}({args})"

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return "".join(f' {key}="{value}"' for key, value in self.props.items())


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None, self_closing=False):
        if value is None:
            raise ValueError("Leaf nodes must have a value")

        if props and not tag:
            raise ValueError("Props can only be provided for nodes with a tag")

        super().__init__(tag, value, props=props, self_closing=self_closing)

    def __repr__(self):
        args = f"{self.tag!r}, {self.value!r}, {self.props!r}, {self.self_closing}"
        return f"{self.__class__.__name__}({args})"

    def to_html(self):
        if self.tag:
            if self.self_closing:
                return f"<{self.tag}{self.props_to_html()} />"
            else:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return self.value


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag:
            raise ValueError("Parent nodes must have a tag")

        if not children:
            raise ValueError("Parent nodes must have children")

        super().__init__(tag, None, children, props)

    def __repr__(self):
        args = f"{self.tag!r}, {self.children!r}, {self.props!r}"
        return f"{self.__class__.__name__}({args})"

    def to_html(self):
        children = "".join(c.to_html() for c in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children}</{self.tag}>"

