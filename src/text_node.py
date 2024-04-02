import re

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
    def __init__(self, markdown, text_type, url=None):
        self.markdown = markdown
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __repr__(self):
        return f"TextNode({self.markdown}, {self.text_type}, {self.url})"

    def to_html_node(self):
        text_type = self.text_type

        if text_type == TT.TEXT:
            return LeafNode(None, self.markdown)
        elif text_type == TT.BOLD:
            return LeafNode("b", self.markdown)
        elif text_type == TT.ITALIC:
            return LeafNode("i", self.markdown)
        elif text_type == TT.CODE:
            return LeafNode("i", self.markdown)
        elif text_type == TT.LINK:
            return LeafNode("a", self.markdown, {"href": self.url})
        elif text_type == TT.IMAGE:
            return LeafNode(
                "img", "", {"src": self.url, "alt": self.markdown}, self_closing=True
            )
        else:
            raise ValueError(f"Unknown text type: {text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue

        if delimiter not in node.markdown:
            new_nodes.append(node)
            continue

        splits = node.markdown.split(delimiter)
        if len(splits) % 2 == 0:
            raise ValueError(f"Delimiter {delimiter!r} not closed in {node.markdown!r}")

        inner = node.markdown.index(delimiter) == 0
        for split in splits:
            tt = text_type if inner else node.text_type
            new_nodes.append(TextNode(split, tt))
            inner = not inner

    return new_nodes


def extract_markdown_images(markdown):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", markdown)


def extract_markdown_links(markdown):
    return re.findall(r"\[(.*?)\]\((.*?)\)", markdown)


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.markdown)
        if not links:
            new_nodes.append(node)
            continue

        markdown = node.markdown
        for link in links:
            md_link = f"[{link[0]}]({link[1]})"
            before, _, markdown = markdown.rpartition(md_link)
            if before:
                new_nodes.append(TextNode(before, node.text_type))

            new_nodes.append(TextNode(link[0], TT.LINK, link[1]))

        if markdown:
            new_nodes.append(TextNode(markdown, node.text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.markdown)
        if not images:
            new_nodes.append(node)
            continue

        markdown = node.markdown
        for image in images:
            md_image = f"![{image[0]}]({image[1]})"
            before, _, markdown = markdown.rpartition(md_image)
            if before:
                new_nodes.append(TextNode(before, node.text_type))

            new_nodes.append(TextNode(image[0], TT.IMAGE, image[1]))

        if markdown:
            new_nodes.append(TextNode(markdown, node.text_type))

    return new_nodes


def text_to_text_nodes(markdown):
    nodes = [TextNode(markdown, TT.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TT.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TT.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TT.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    return

