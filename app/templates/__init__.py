from pathlib import Path

from promplate import Template

root = Path(__file__).parent

one_pass = Template.read(root / "one-pass.j2")


__all__ = ["one_pass"]
