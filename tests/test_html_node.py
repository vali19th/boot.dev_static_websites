import pytest


from src.html_node import HTMLNode, LeafNode, ParentNode


def test_HTMLNode():
    n = HTMLNode("p", None, None, None).props_to_html() == ""
    n = HTMLNode(None, "Hello", None, None).props_to_html() == ""

    n = HTMLNode("div", None, None, {"id": "main", "class": "flex"})
    assert n.props_to_html() == ' id="main" class="flex"'

    with pytest.raises(ValueError):
        HTMLNode()


def test_LeafNode():
    n = LeafNode(None, "Hello, World!").to_html() == "Hello, World!"

    n = LeafNode("p", "This is a paragraph of text.")
    assert n.to_html() == "<p>This is a paragraph of text.</p>"

    n = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    assert n.to_html() == '<a href="https://www.google.com">Click me!</a>'

    with pytest.raises(ValueError):
        LeafNode("p", None)


def test_ParentNode():
    n = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
    assert n.to_html() == expected

    n = ParentNode(
        "html",
        [
            ParentNode("head", [LeafNode("title", "My Webpage")]),
            ParentNode(
                "body",
                [
                    ParentNode(
                        "div", [LeafNode("p", "Hello, World!")], {"class": "flex"}
                    )
                ],
            ),
        ],
    )

    head = "<head><title>My Webpage</title></head>"
    body = '<body><div class="flex"><p>Hello, World!</p></div></body>'
    assert n.to_html() == f"<html>{head}{body}</html>"

