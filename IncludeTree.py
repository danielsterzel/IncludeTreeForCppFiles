from NodeObject import NodeObject
from dataclasses import dataclass
from collections import defaultdict
from collections import Counter


@dataclass
class IncludeTree:
    nodes: list[NodeObject]

    @property
    def roots(self) -> list[NodeObject]:
        return [n for n in self.nodes if n.parent is None]

    def __getitem__(self, item):
        return self.nodes[item]

    def levels(self):
        levels = defaultdict(list)
        for node in self.nodes:
            levels[node.depth].append(node)
        return dict(levels)

    @staticmethod
    def print_subtree(node, indent=0):
        print("  " * indent + node.name)
        for child in node.children:
            IncludeTree.print_subtree(child, indent + 1)

    def find(self, name: str) -> list[NodeObject]:
        return [n for n in self.nodes if n.name == name]

    def why(self, name: str):
        for node in self.find(name):
            print(" ----- > ".join(node.path()))

    def what(self, name: str):
        for node in self.find(name):
            IncludeTree.print_subtree(node)

    def duplicate(self):
        counts = Counter(node.name for node in self.nodes)

        duplicates = defaultdict(list)
        for node in self.nodes:
            if counts[node.name] > 1:
                duplicates[node.name].append(node)

        return dict(duplicates)

    def view(self):
        # later probable graph visualization with network something something package
        pass
