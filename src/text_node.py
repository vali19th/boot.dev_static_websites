import re
import textwrap

from enum import Enum
from pprint import pprint

from html_node import ParentNode, LeafNode


class TT(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class BT(Enum):
    PARAGRAPH = "p"
    HEADING = "heading"
    CODE = "pre"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


class TextNode:
    def __init__(self, markdown, text_type, url=None):
        self.markdown = markdown
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __repr__(self):
        args = f"{self.markdown!r}, {self.text_type!r}, {self.url!r}"
        return f"{self.__class__.__name__}({args})"

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


def markdown_to_text_nodes(markdown):
    nodes = [TextNode(markdown, TT.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TT.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TT.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TT.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [textwrap.dedent(b).strip() for b in blocks if b]


def block_to_block_type(block):
    if block.startswith("#"):
        return BT.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BT.CODE
    elif block.startswith(">"):
        return BT.QUOTE
    elif block.startswith(("- ", "* ")):
        return BT.UNORDERED_LIST
    elif re.search(r"^\d+\.", block):
        return BT.ORDERED_LIST
    else:
        return BT.PARAGRAPH


def markdown_to_html_node(markdown):
    """
    Quote blocks should be surrounded by a <blockquote> tag.
    Unordered list blocks should be surrounded by a <ul> tag, and each list item should be surrounded by a <li> tag.
    Code blocks should be surrounded by a <code> tag nested inside a <pre> tag.
    Paragraphs should be surrounded by a <p> tag.
    """

    block_nodes = []
    for b in markdown_to_blocks(markdown):
        b_type = block_to_block_type(b)

        # fmt: off
        if   b_type == BT.PARAGRAPH:      node = block_to_html_p(b)
        elif b_type == BT.HEADING:        node = block_to_html_heading(b)
        elif b_type == BT.CODE:           node = block_to_html_pre(b)
        elif b_type == BT.QUOTE:          node = block_to_html_blockquote(b)
        elif b_type == BT.UNORDERED_LIST: node = block_to_html_ul(b)
        elif b_type == BT.ORDERED_LIST:   node = block_to_html_ol(b)
        # fmt: on

        print("\n\n")
        print("b", repr(b))
        print("b_type", repr(b_type))
        print("node", repr(node))
        block_nodes.append(node)
        x = [...]

    return ParentNode("div", block_nodes)


def block_to_html_p(block):
    return


def block_to_html_heading(block):
    n = block.count("#")
    children = block.strip("#").strip()
    children = markdown_to_text_nodes(children)
    children = [c.to_html_node() for c in children]
    return ParentNode(f"h{n}", children)


def block_to_html_pre(block):
    block = block.strip("```").strip()
    return ParentNode("pre", [LeafNode(None, block)])


def block_to_html_blockquote(block):
    return


def block_to_html_ul(block):
    children = []
    for item in block.split("\n"):
        item = re.sub(r"^[-*] ", "", item)
        children.append(ParentNode("li", [LeafNode(None, item)]))

    return ParentNode("ul", children)


def block_to_html_ol(block):
    children = []
    for item in block.split("\n"):
        item = re.sub(r"^\d+\. ", "", item)
        children.append(ParentNode("li", [LeafNode(None, item)]))

    return ParentNode("ol", children)

