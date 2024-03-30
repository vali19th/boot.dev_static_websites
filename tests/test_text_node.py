from src.text_node import TextNode


def test_equality():
    assert TextNode("text", "bold") == TextNode("text", "bold")

    n = TextNode("text", "bold", "http://www.x.com")
    n_2 = TextNode("text", "bold", "http://www.x.com")
    assert n == n_2

    assert TextNode("text", "bold") != TextNode("text", "italic")
    assert TextNode("text", "bold", "http://www.x.com") != TextNode("text", "bold")


def test_to_html_node():
    n = TextNode("text", "text").to_html_node()
    assert n.to_html() == "text"

    n = TextNode("text", "bold").to_html_node()
    assert n.to_html() == "<b>text</b>"

    n = TextNode("text", "italic").to_html_node()
    assert n.to_html() == "<i>text</i>"

    n = TextNode("text", "code").to_html_node()
    assert n.to_html() == "<i>text</i>"

    n = TextNode("text", "link", "http://www.x.com").to_html_node()
    assert n.to_html() == '<a href="http://www.x.com">text</a>'

    n = TextNode("Twitter", "image", "http://www.x.com").to_html_node()
    assert n.to_html() == '<img src="http://www.x.com" alt="Twitter" />'

