class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html is not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""

        res = []
        for key, value in self.props.items():
            res.append(f'{key}="{value}"')
        return " ".join(res)

    def __repr__(self):
        return f"HTMLNode ({self.tag}\n {self.value}\n {self.children}\n {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf nodes must have a value")

        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode ({self.tag}\n {self.value}\n {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have a children")

        children_html = "".join([child.to_html() for child in self.children])

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
