from enum import Enum

from html_node import LeafNode


class TT(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def to_html_node(self):
        text_type = self.text_type

        if text_type == TT.TEXT:
            return LeafNode(None, self.text)
        elif text_type == TT.BOLD:
            return LeafNode("b", self.text)
        elif text_type == TT.ITALIC:
            return LeafNode("i", self.text)
        elif text_type == TT.CODE:
            return LeafNode("i", self.text)
        elif text_type == TT.LINK:
            return LeafNode("a", self.text, {"href": self.url})
        elif text_type == TT.IMAGE:
            return LeafNode(
                "img", "", {"src": self.url, "alt": self.text}, self_closing=True
            )
        else:
            raise ValueError(f"Unknown text type: {text_type}")


# def split_nodes_delimiter(old_nodes, delimiter, text_type):

