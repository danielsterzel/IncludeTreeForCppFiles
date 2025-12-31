from dataclasses import dataclass, field
from typing import Optional, List
import os


@dataclass
class NodeObject:
    depth: int
    full_include_path: str
    parent: Optional["NodeObject"] = None
    children: List["NodeObject"] = field(default_factory=list)

    @property
    def name(self) -> str:
        return os.path.basename(self.full_include_path)

    @property
    def is_system(self) -> bool:
        return (
            "include/c++" in self.full_include_path
            or self.full_include_path.startswith("/usr/")
            or "Cellar/llvm" in self.full_include_path
        )

    def is_project_file(self, repo_root: str) -> bool:
        return self.full_include_path.startswith(repo_root)

    def path(self) -> list[str]:
        """ " Returns include path from root to this node"""
        node = self
        include_branch = []
        while node:
            include_branch.append(node.name)
            node = node.parent
        return list(reversed(include_branch))

    @classmethod
    def from_raw(cls, obj):
        """ "
        Convert supported input types into NodeObject
        """
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, tuple) and len(obj) == 2:
            depth, line = obj
            return cls(depth, line)

        raise TypeError(f"Cannot convert {type(obj)} to NodeObject")
