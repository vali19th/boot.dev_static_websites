import textwrap

from pprint import pprint

import pytest

from src.html_node import ParentNode, LeafNode
from src.text_node import (
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    markdown_to_html_node,
    markdown_to_text_nodes,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    TextNode,
    BT,
    TT,
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
    # leave the empty lines in. We must test that we do not create empty blocks
    markdown = """
        This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line




        * This is a list
        * with items
    """

    b1 = "This is **bolded** paragraph"
    b2 = """
        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line
    """
    b3 = """
        * This is a list
        * with items
    """

    blocks = [b1, b2, b3]
    blocks = [textwrap.dedent(b).strip() for b in blocks]
    assert markdown_to_blocks(markdown) == blocks


@pytest.mark.parametrize(
    "md, block_type",
    [
        ("```print('Hello, World!')\n```", BT.CODE),
        ("# h1", BT.HEADING),
        ("###### h6", BT.HEADING),
        ("> This is a blockquote\n> with multiple lines", BT.QUOTE),
        ("* milk\n* eggs", BT.UNORDERED_LIST),
        ("- milk\n- eggs", BT.UNORDERED_LIST),
        ("1. milk\n2. eggs", BT.ORDERED_LIST),
        ("This is a paragraph.", BT.PARAGRAPH),
    ],
)
def test_block_to_block_type(md, block_type):
    block = markdown_to_blocks(md)[0]
    assert block_to_block_type(block) == block_type


def test_markdown_to_html_node():
    markdown = """
        ```
        print('Hello, World!')
        ```

        # heading 1

        ## heading 2

        ### heading 3

        #### heading 4

        ##### heading 5

        ###### heading 6

        > This is a blockquote
        > with multiple lines

        * milk
        * eggs

        - milk
        - eggs

        1. milk
        2. eggs

        This is an **awesome** paragraph.
    """

    markdown = """
        ```
        print('Hello, World!')
        ```

        # heading 1

        ## heading 2

        ### heading 3

        #### heading 4

        ##### heading 5

        ###### heading 6

        * milk
        * eggs

        - milk
        - eggs

        1. milk
        2. eggs
    """

    expected = ParentNode(
        "div",
        [
            ParentNode("pre", [LeafNode(None, "print('Hello, World!')")]),
            ParentNode("h1", [LeafNode(None, "heading 1")]),
            ParentNode("h2", [LeafNode(None, "heading 2")]),
            ParentNode("h3", [LeafNode(None, "heading 3")]),
            ParentNode("h4", [LeafNode(None, "heading 4")]),
            ParentNode("h5", [LeafNode(None, "heading 5")]),
            ParentNode("h6", [LeafNode(None, "heading 6")]),
            #     ParentNode(
            #         "blockquote",
            #         [
            #             LeafNode(None, "This is a blockquote"),
            #             LeafNode(None, "with multiple lines"),
            #         ],
            #     ),
            ParentNode(
                "ul",
                [
                    ParentNode("li", [LeafNode(None, "milk")]),
                    ParentNode("li", [LeafNode(None, "eggs")]),
                ],
            ),
            ParentNode(
                "ul",
                [
                    ParentNode("li", [LeafNode(None, "milk")]),
                    ParentNode("li", [LeafNode(None, "eggs")]),
                ],
            ),
            ParentNode(
                "ol",
                [
                    ParentNode("li", [LeafNode(None, "milk")]),
                    ParentNode("li", [LeafNode(None, "eggs")]),
                ],
            ),
            #     ParentNode(
            #         "p",
            #         [
            #             LeafNode(None, "This is an "),
            #             LeafNode("bold", "**awesome**"),
            #             LeafNode(None, " paragraph."),
            #         ],
            #     ),
        ],
    )

    actual = markdown_to_html_node(markdown)
    print("ACTUAL", actual)
    actual = actual.to_html()
    expected = expected.to_html()

    print("\n\n")
    print("--------- START")
    print("markdown", repr(markdown))
    print("actual  ", repr(actual))
    print("expected", repr(expected))
    print("eq", actual == expected)
    print("eq", repr(actual) == repr(expected))
    print("--------- END")

    assert actual == expected

