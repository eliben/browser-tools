from __future__ import annotations

import html
import re
from pathlib import Path
from typing import List, Tuple


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


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


def render_inline_markdown(text: str) -> str:
    """Render a minimal subset of markdown (inline links) into HTML."""
    parts: List[str] = []
    last = 0
    for match in LINK_RE.finditer(text):
        parts.append(html.escape(text[last:match.start()]))
        label = html.escape(match.group(1))
        url = html.escape(match.group(2), quote=True)
        parts.append(f'<a href="{url}">{label}</a>')
        last = match.end()
    parts.append(html.escape(text[last:]))
    return "".join(parts)


def parse_list_item(text: str) -> Tuple[str, str, str]:
    """Parse a markdown bullet into (title, url, description_html)."""
    match = LINK_RE.search(text)
    if not match:
        raise RuntimeError(f"Could not find a link in list item: {text}")

    title = match.group(1).strip()
    url = match.group(2).strip()
    remainder = text[match.end():].strip()
    if remainder.startswith(("-", "–", "—")):
        remainder = remainder[1:].strip()
    description = render_inline_markdown(remainder) if remainder else ""
    return title, url, description


def parse_list_items(lines: List[str]) -> List[Tuple[str, str, str]]:
    """Parse markdown list items into (title, url, description)."""
    items: List[Tuple[str, str, str]] = []

    buffer = ""
    for line in lines:
        if line.lstrip().startswith("* "):
            if buffer:
                items.append(parse_list_item(buffer.strip().lstrip("*").strip()))
            buffer = line.strip()
        elif buffer:
            buffer += " " + line.strip()

    if buffer:
        items.append(parse_list_item(buffer.strip().lstrip("*").strip()))

    return items


def render_html(tools: List[Tuple[str, str, str]]) -> str:
    """Render the extracted tools list to a minimal HTML page."""
    lines = [
        "<!doctype html>",
        "<html>",
        "<head>",
        '  <meta charset="utf-8">',
        "  <title>eliben browser-tools</title>",
        "  <style>",
        "    body {",
        '      font-family: Roboto, "Segoe UI", sans-serif;',
        "      font-size: 1.15rem;",
        "      line-height: 1.5;",
        "      margin: 0;",
        "      padding: 24px;",
        "    }",
        "",
        "    a,",
        "    a:visited {",
        "      color: #0b57d0;",
        "    }",
        "",
        "    a:hover {",
        "      color: #c5221f;",
        "    }",
        "  </style>",
        "</head>",
        "<body>",
        "  See <a href=\"https://github.com/eliben/browser-tools\">the GitHub repository</a> for details",
        "  <h1>List of tools</h1>",
        "  <ul>",
    ]

    for title, url, desc in tools:
        li = f'    <li><a href="{html.escape(url, quote=True)}">{html.escape(title)}</a>'
        if desc:
            li += f" - {desc}"
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
