from NodeObject import NodeObject
from dataclasses import dataclass, field


@dataclass
class IncludeTreeLevel:
    nth_tree_depth_level_nodes: list = field(
        default_factory=list
    )  # create a new object for each instance

    @classmethod
    def from_raw(cls, node_list):
        if isinstance(node_list, cls):
            return node_list
        if isinstance(node_list, list) and not isinstance(node_list, (str, bytes)):
            return cls(node_list)

        raise TypeError(f"Cannot convert {type(node_list)} to IncludeTreeLevel")

    def __post_init__(self):
        self.nth_tree_depth_level_nodes = [
            node if isinstance(node, NodeObject) else NodeObject.from_raw(node)
            for node in self.nth_tree_depth_level_nodes
        ]

    def __getitem__(self, item):
        return self.nth_tree_depth_level_nodes[item]

    def view(self):
        print(self.nth_tree_depth_level_nodes)

    def check_is_included(self, substr: str):
        if not isinstance(substr, str):
            raise TypeError(f"Argument {substr} should be a string")

        is_included = False
        for node in self.nth_tree_depth_level_nodes:
            if substr not in node.full_include_path:
                continue
            is_included = True
        if is_included:
            print(
                f"include: {substr} found at level: {self.nth_tree_depth_level_nodes[0].depth}"
            )
            print(self.nth_tree_depth_level_nodes)
        else:
            print(
                "include not found at level: {self.nth_tree_depth_level_nodes[0].depth}"
            )
