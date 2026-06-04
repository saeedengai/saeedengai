"""
Generate README.md for the GitHub profile from data/profile.json.

How it works:
  1. Load the content from data/profile.json into a Python dictionary.
  2. Load the layout from templates/readme_template.md.
  3. Replace every {{placeholder}} in the template with the matching content.
  4. Write the finished result to README.md.

To update your profile:
  - Edit data/profile.json (add a skill, change a link, etc.)
  - Run:  python generate.py
  - Commit and push.
"""

import json
from pathlib import Path

# Paths are relative to this script, so it works no matter where you run it from.
ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "profile.json"
TEMPLATE_FILE = ROOT / "templates" / "readme_template.md"
OUTPUT_FILE = ROOT / "README.md"


def render_roles(roles):
    """Join the roles list into one line separated by ' | '."""
    return " | ".join(roles)


def render_skills(skills):
    """Turn the skills dict into a bulleted list, one line per category."""
    lines = [f"- **{category}:** " + ", ".join(items)
             for category, items in skills.items()]
    return "\n".join(lines)


def render_links(links):
    """Turn the links list into a bulleted list of markdown links."""
    return "\n".join(f"- [{item['name']}]({item['url']})" for item in links)


def main():
    # 1. Load content (JSON -> dict) and layout (template -> text)
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    template = TEMPLATE_FILE.read_text(encoding="utf-8")

    # 2. Build the value for each placeholder
    replacements = {
        "greeting": data["greeting"],
        "name": data["name"],
        "tagline": data["tagline"],
        "roles": render_roles(data["roles"]),
        "about": data["about"],
        "skills": render_skills(data["skills"]),
        "links": render_links(data["links"]),
        "footer": data["footer"],
    }

    # 3. Swap every {{placeholder}} in the template for its value
    output = template
    for key, value in replacements.items():
        output = output.replace("{{" + key + "}}", value)

    # 4. Write the finished README
    OUTPUT_FILE.write_text(output, encoding="utf-8")
    print(f"README.md generated successfully ({len(output)} characters).")


if __name__ == "__main__":
    main()
