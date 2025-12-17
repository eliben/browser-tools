from __future__ import annotations

import html
import re
from pathlib import Path
from typing import List, Tuple


def extract_section(lines: List[str]) -> List[str]:
    """Return lines under the '## List of tools' heading until the next heading."""
    start = None
    for idx, line in enumerate(lines):
        if line.strip().lower() == "## list of tools":
            start = idx + 1
            break

    if start is None:
        raise RuntimeError("Could not find '## List of tools' heading in README.md")

    section: List[str] = []
    for line in lines[start:]:
        if line.startswith("#"):
            break
        section.append(line)

    return section


def parse_list_items(lines: List[str]) -> List[Tuple[str, str, str]]:
    """Parse markdown list items into (title, url, description). Assumes well-formed bullets."""
    items: List[Tuple[str, str, str]] = []
    pattern = re.compile(r"\* \[([^\]]+)\]\(([^)]+)\)\s*-\s*(.+)")

    buffer = ""
    for line in lines:
        if line.lstrip().startswith("* "):
            if buffer:
                match = pattern.match(buffer.strip())
                if not match:
                    raise RuntimeError(f"Could not parse list item: {buffer}")
                items.append(match.groups())
            buffer = line.strip()
        elif buffer:
            buffer += " " + line.strip()

    if buffer:
        match = pattern.match(buffer.strip())
        if not match:
            raise RuntimeError(f"Could not parse list item: {buffer}")
        items.append(match.groups())

    return items


def render_html(tools: List[Tuple[str, str, str]]) -> str:
    """Render the extracted tools list to a minimal HTML page."""
    lines = [
        "<!doctype html>",
        "<html>",
        "<head>",
        '  <meta charset="utf-8">',
        "  <title>eliben browser-tools</title>",
        "</head>",
        "<body>",
        "  See <a href=\"https://github.com/eliben/browser-tools\">the GitHub repository</a> for details",
        "  <h1>List of tools</h1>",
        "  <ul>",
    ]

    for title, url, desc in tools:
        li = f'    <li><a href="{html.escape(url, quote=True)}">{html.escape(title)}</a>'
        if desc:
            li += f" - {html.escape(desc)}"
        li += "</li>"
        lines.append(li)

    lines.extend(
        [
            "  </ul>",
            "</body>",
            "</html>",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    readme_path = Path("README.md")
    index_path = Path("index.html")

    readme_lines = readme_path.read_text(encoding="utf-8").splitlines()
    section_lines = extract_section(readme_lines)
    tools = parse_list_items(section_lines)
    html_output = render_html(tools)

    index_path.write_text(html_output, encoding="utf-8")
    print(f"Wrote {index_path}")


if __name__ == "__main__":
    main()
