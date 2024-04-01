from src.text_node import TextNode, TT


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

