import sys
import traceback

from text_node import TextNode


def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(node)


if __name__ == "__main__":
    try:
        r = main() or 0
    except:
        traceback.print_exc()
        r = 1

    sys.exit(r)

