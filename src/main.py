import re
import shutil

from pathlib import Path

from text_node import markdown_to_html_node


def main():
    copy_dir("static", "public")
    generate_pages_recursive("content", "content/template.html", "public")


def generate_pages_recursive(src_dir, template_path, dest_dir):
    for p in Path(src_dir).iterdir():
        dest_name = Path(dest_dir).joinpath(p.name)
        if p.is_dir():
            generate_pages_recursive(p, template_path, dest_name)
        elif p.is_file() and p.suffix == ".md":
            generate_page(p, template_path, dest_name.with_suffix(".html"))


def generate_page(src_path, template_path, dest_path):
    print(
        f"[INFO] Generating page from {str(src_path)!r} -> {str(dest_path)!r} using {str(template_path)!r}"
    )

    src_path = Path(src_path)
    template_path = Path(template_path)
    dest_path = Path(dest_path)

    src = src_path.read_text()
    template = template_path.read_text()

    html = markdown_to_html_node(src).to_html()
    title = extract_title(html)
    formatted = template.replace("{{ title }}", title).replace("{{ content }}", html)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(formatted)


def extract_title(html):
    h1_tags = re.findall(r"<h1>(.*?)</h1>", html)
    if not h1_tags:
        raise ValueError("No title found")
    elif len(h1_tags) >= 2:
        raise ValueError("Too many titles found")
    else:
        return h1_tags[0].title()


def copy_dir(src, dest):
    dest = Path(dest)
    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
        print(f"[INFO] Deleted dir {str(dest)!r}")

    dest.mkdir()
    print(f"[INFO] Created dir {str(dest)!r}")

    for p in Path(src).iterdir():
        dest_p = dest.joinpath(p.name)

        if p.is_file():
            shutil.copyfile(p, dest_p)
            print(f"[INFO] Copied {str(p)!r} to {str(dest_p)!r}")
        else:
            copy_dir(p, dest_p)


if __name__ == "__main__":
    main()

