import re
import shutil

from pathlib import Path

from text_node import markdown_to_html_node


def main():
    copy_dir("static", "public")

    src = "content/index.md"
    template = "src/template.html"
    dest = "public/index.html"
    generate_page(src, template, dest)


def generate_page(src_path, template_path, dest_path):
    print(
        f"\n[INFO] Generating page from {src_path!r} -> {dest_path!r} using {template_path!r}"
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

