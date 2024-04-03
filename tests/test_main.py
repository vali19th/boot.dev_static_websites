import pytest

from text_node import markdown_to_html_node
from main import extract_title


def test_extract_title():
    md = """
        # helo world

        ## Hellowwww World!

        asdadas
    """

    html = markdown_to_html_node(md).to_html()
    assert extract_title(html) == "Helo World"

    md = """
        # helo world

        # Hellowwww World!
    """

    html = markdown_to_html_node(md).to_html()
    with pytest.raises(ValueError):
        extract_title(html)

    md = "## helo world"
    html = markdown_to_html_node(md).to_html()
    with pytest.raises(ValueError):
        extract_title(html)

