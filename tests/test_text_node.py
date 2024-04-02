from pprint import pprint
from src.text_node import (
    TextNode,
    TT,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    markdown_to_text_nodes,
)


def test_equality():
    assert TextNode("text", TT.BOLD) == TextNode("text", TT.BOLD)

    n = TextNode("text", TT.BOLD, "http://www.x.com")
    n_2 = TextNode("text", TT.BOLD, "http://www.x.com")
    assert n == n_2

    assert TextNode("text", TT.BOLD) != TextNode("text", TT.ITALIC)
    assert TextNode("text", TT.BOLD, "http://www.x.com") != TextNode("text", TT.BOLD)


def test_to_html_node():
    n = TextNode("text", TT.TEXT).to_html_node()
    assert n.to_html() == "text"

    n = TextNode("text", TT.BOLD).to_html_node()
    assert n.to_html() == "<b>text</b>"

    n = TextNode("text", TT.ITALIC).to_html_node()
    assert n.to_html() == "<i>text</i>"

    n = TextNode("text", TT.CODE).to_html_node()
    assert n.to_html() == "<i>text</i>"

    n = TextNode("text", TT.LINK, "http://www.x.com").to_html_node()
    assert n.to_html() == '<a href="http://www.x.com">text</a>'

    n = TextNode("Twitter", TT.IMAGE, "http://www.x.com").to_html_node()
    assert n.to_html() == '<img src="http://www.x.com" alt="Twitter" />'


def test_md_to_text_node():
    node = TextNode("This is text with a **bolded** word", TT.TEXT)
    assert split_nodes_delimiter([node], "**", TT.BOLD) == [
        TextNode("This is text with a ", TT.TEXT),
        TextNode("bolded", TT.BOLD),
        TextNode(" word", TT.TEXT),
    ]

    node = TextNode("This is text with a `code block` word", TT.TEXT)
    assert split_nodes_delimiter([node], "`", TT.CODE) == [
        TextNode("This is text with a ", TT.TEXT),
        TextNode("code block", TT.CODE),
        TextNode(" word", TT.TEXT),
    ]


def test_extract_markdown_images():
    markdown = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
    assert extract_markdown_images(markdown) == [
        ("image", "https://i.imgur.com/zjjcJKZ.png"),
        ("another", "https://i.imgur.com/dfsdkjfd.png"),
    ]


def test_extract_markdown_links():
    markdown = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    assert extract_markdown_links(markdown) == [
        ("link", "https://www.example.com"),
        ("another", "https://www.example.com/another"),
    ]


def test_split_nodes_image():
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png).",
        TT.TEXT,
    )
    pprint(split_nodes_image([node]))
    assert split_nodes_image([node]) == [
        TextNode("This is text with an ", TT.TEXT),
        TextNode("image", TT.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TT.TEXT),
        TextNode("second image", TT.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        TextNode(".", TT.TEXT),
    ]


def test_split_nodes_link():
    node = TextNode(
        "This is text with an [link](https://x.com/) and another [second link](https://youtube.com/).",
        TT.TEXT,
    )
    pprint(split_nodes_link([node]))
    assert split_nodes_link([node]) == [
        TextNode("This is text with an ", TT.TEXT),
        TextNode("link", TT.LINK, "https://x.com/"),
        TextNode(" and another ", TT.TEXT),
        TextNode("second link", TT.LINK, "https://youtube.com/"),
        TextNode(".", TT.TEXT),
    ]


def test_text_to_text_nodes():
    markdown = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
    assert markdown_to_text_nodes(markdown) == [
        TextNode("This is ", TT.TEXT),
        TextNode("text", TT.BOLD),
        TextNode(" with an ", TT.TEXT),
        TextNode("italic", TT.ITALIC),
        TextNode(" word and a ", TT.TEXT),
        TextNode("code block", TT.CODE),
        TextNode(" and an ", TT.TEXT),
        TextNode("image", TT.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and a ", TT.TEXT),
        TextNode("link", TT.LINK, "https://boot.dev"),
    ]


def test_markdown_to_blocks():
    markdown = """
        This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items
    """

