#!/usr/bin/env python3

import argparse
import os
import subprocess
import shutil
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional, List


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

    def path(self) -> list[str]:
        node = self
        result = []
        while node:
            result.append(node.name)
            node = node.parent
        return list(reversed(result))

    def __repr__(self) -> str:
        return f"NodeObject(name='{self.name}', depth={self.depth})"


@dataclass
class IncludeTree:
    nodes: list[NodeObject]

    def find(self, name: str) -> list[NodeObject]:
        return [n for n in self.nodes if n.name == name or n.name == f"{name}.h"]

    def why(self, name: str, project_only=False):
        matches = self.find(name)
        if not matches:
            print(f"No include named '{name}' found")
            return

        for node in matches:
            if project_only and node.is_system:
                continue
            print(" → ".join(node.path()))

    def what(self, name: str, project_only=False):
        matches = self.find(name)
        if not matches:
            print(f"No include named '{name}' found")
            return

        for node in matches:
            self._print_subtree(node, project_only=project_only)

    def duplicates(self):
        counts = Counter(n.name for n in self.nodes)
        for name, count in counts.items():
            if count > 1:
                print(f"{name}: {count} times")

    def _print_subtree(self, node, indent=0, project_only=False):
        if project_only and node.is_system:
            return
        if node.name.startswith("__"):
            return
        print("  " * indent + node.name)
        for child in node.children:
            self._print_subtree(child, indent + 1, project_only)


def build_tree(source_file: str) -> IncludeTree:
    if shutil.which("clang++") is None:
        raise RuntimeError("clang++ not found")

    tmp_file = ".include_graph_tmp.txt"

    with open(tmp_file, "w") as f:
        subprocess.run(
            ["clang++", "-E", "-H", source_file, "-I", os.getcwd()],
            stdout=subprocess.DEVNULL,
            stderr=f,
            check=False,
            text=True,
        )
    root = NodeObject(depth=0, full_include_path=source_file)
    stack: list[NodeObject] = [root]
    nodes: list[NodeObject] = [root]

    with open(tmp_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith('.'):
                continue
            dots, path = line.split(' ', 1)
            depth = dots.count('.')
            node = NodeObject(depth, path)

            while stack and stack[-1].depth >= depth:
                stack.pop()

            if stack:
                node.parent = stack[-1]
                stack[-1].children.append(node)

            stack.append(node)
            nodes.append(node)

    os.remove(tmp_file)
    return IncludeTree(nodes)


def main():
    parser = argparse.ArgumentParser(description="cpp include graph tool")
    parser.add_argument("file", help=".h or .cpp file")
    parser.add_argument("command", choices=["why", "what", "duplicates"])
    parser.add_argument("name", nargs="?", help="header name (e.g. vector)")
    parser.add_argument(
        "--project-only", action="store_true", help="hide system headers"
    )
    # parser.add_argument(" --root", help="Project root used as -I (default: current dir)")
    args = parser.parse_args()
    tree = build_tree(args.file)

    if args.command == "why":
        if not args.name:
            parser.error("why requires a header name")
        tree.why(args.name, project_only=args.project_only)
    elif args.command == "what":
        if not args.name:
            parser.error("what requires a header name")
        tree.what(args.name, project_only=args.project_only)
    elif args.command == "duplicates":
        tree.duplicates()


if __name__ == "__main__":
    main()
