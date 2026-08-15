# /// script
# requires-python = ">=3.13"
# dependencies = ["htpy"]
# ///
"""
Bundle all browser extensions into zip files and also generate an index page for them.

"""
import json
import subprocess
from collections import namedtuple
from pathlib import Path

from htpy import a as anchor
from htpy import body, div, h1, h2, head, html, meta, style, title

HERE = Path(__file__).parent

build_dir = HERE / "_build"
if not build_dir.exists():
    build_dir.mkdir()

index_file = build_dir / "index.html"


Extension = namedtuple("Extension", ["name", "description", "file"])


def main():
    extensions: list[Extension] = []

    for ext_dir in Path(HERE).glob("*-extension"):
        zip_file = build_dir / f"{ext_dir.name}.zip"
        cmd = ["zip", "-r", zip_file, ext_dir]
        subprocess.run(cmd, check=False)

        manifest_file = ext_dir / "manifest.json"
        manifest = json.loads(manifest_file.read_text())
        extension = Extension(
            manifest["name"],
            manifest["description"],
            zip_file,
        )
        extensions.append(extension)

    generate_index_page(extensions)


def layout(content):
    title_text = "Browser Extensions"

    return html[
        head[
            meta(charset="utf-8"),
            meta(
                name="viewport",
                content="width=device-width, initial-scale=1.0, viewport-fit=cover",
            ),
            title[title_text],
            style["""
            .row {
                display: flex;
                flex-direction: row;
                align-items: center;
                gap: 1em;
            }
            """],
        ],
        body[
            h1[title_text],
            *content,
        ],
    ]


def generate_index_page(extensions):
    doc = layout(
        div[div(class_='row')[h2[e.name], anchor(href=e.file.name)["Download"]], div[e.description]]
        for e in extensions
    )

    with index_file.open("w") as fp:
        fp.write(str(doc))


if __name__ == "__main__":
    main()
