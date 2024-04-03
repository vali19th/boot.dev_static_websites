import sys
import shutil
import traceback

from pathlib import Path


def main():
    copy_dir("static", "public")


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
    try:
        r = main() or 0
    except:
        traceback.print_exc()
        r = 1

    sys.exit(r)

