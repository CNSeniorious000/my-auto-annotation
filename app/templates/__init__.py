from pathlib import Path

from promplate import Template

root = Path(__file__).parent

prompt = Template.read(root / "prompt.j2")


__all__ = ["prompt"]
