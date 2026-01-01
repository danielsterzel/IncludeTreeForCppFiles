# ============================= # Include Graph # =============================
# This endeavour is set to answer these questions:
#  1.For includes:
#       - Why is this header here?
#       - Is it included in another path?
#       - What is the shortest path of includes?
# 2. For function calls:
#       - What calls a specific function?
#       - What is the call path of a specific function?
#
# All this information pertains to a gtest environment in C++ code and unit test code. The bellow mentioned mock
# problem is defined as follows: "Where exactly in source code is this function called or not called (depending
# on the gtest run output)?".
#
# Example output (includes):
#   main.cpp
#       24 headers included (unique)
#       2 headers reachable from multiple paths
# After clicking a "▼":
#   b.h
#       Path 1: main.cpp → a.h → b.h
#       Path 2: main.cpp → d.h → b.h
#
# Example output (mock problem):
#   `foo() called from test
#       - 2 possible call paths`
# Again after clicking "▼":
#   Path1:
#     TestBody → fizzBuzz() → bar() → foo()
#   Path2:
#     TestBody → helper() → buzzFizz() → foo()
# =============================================================================
from NodeObject import NodeObject
from IncludeTreeLevel import IncludeTreeLevel
from IncludeTree import IncludeTree


def debug(*args):
    print("DEBUG PRINT USE ONLY IN DEVELOPMENT")
    print(*args)


import os
import shutil
import subprocess

from collections import defaultdict

home_path = os.path.expanduser("~")
path_string = "Desktop/main.cpp"
file_path = os.path.join(home_path, path_string)
if not os.path.exists(file_path):
    raise Exception(f"Path: {file_path} does not exist")
if shutil.which("clang++") is None:
    # maybe use custom script for building tree here if clang not found?
    raise Exception(f"Clang compiler not found, please install it first")

# output_path = os.path.join(home_path, "Desktop/tree.txt")
file_path = os.path.join("/Users/danielsterzel/PycharmProjects/IncludeTree", "main.cpp")

output_path = os.path.join("/Users/danielsterzel/PycharmProjects/IncludeTree", "tree.txt")
with open(output_path, "w") as f:
    subprocess.run(
        ["clang++", "-E", "-H", file_path, "-I", "/Users/danielsterzel/PycharmProjects/IncludeTree"],
        stdout=subprocess.DEVNULL,
        stderr=f,
        check=False,
        text=True,
    )
print(f"Include tree written to  {output_path}")

root = NodeObject(depth=0, full_include_path=file_path)
stack: list[NodeObject] = [root]
all_nodes: list[NodeObject] = [root]

with open(output_path, "r") as f:

    for line in f:
        line = line.strip()
        if not line.startswith("."):
            continue

        dots, path = line.split(" ", 1)
        depth = dots.count(".")

        # include_depth, include_path = line.split("/", 1)
        # depth = include_depth.count(".")
        # include_path = include_path.rstrip()
        node = NodeObject.from_raw((depth, path))

        while stack and stack[-1].depth >= depth:
            stack.pop()

        if stack:
            node.parent = stack[-1]
            stack[-1].children.append(node)
        stack.append(node)
        all_nodes.append(node)

include_tree = IncludeTree(nodes=all_nodes)

# print("What includes vector?")
# include_tree.why("vector")
# print("What does vector include?")
# include_tree.what("vector")

include_tree.what("file.h")
include_tree.why("file.h")
# matches = include_tree.find("file.h")
# print("FOUND:", matches)
