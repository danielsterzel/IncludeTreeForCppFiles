from NodeObject import NodeObject
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class IncludeTree:
    nodes: list[NodeObject]

    @property
    def roots(self) -> list[NodeObject]:
        return [n for n in self.nodes if n.parent is None]

    def levels(self):
        levels = defaultdict(list)
        for node in self.nodes:
            levels[node.depth].append(node)
        return dict(levels)

    def view(self):
        # later probable graph visualization with network something something package
        pass
