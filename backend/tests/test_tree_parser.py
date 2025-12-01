import pytest
from app.utils.tree_parser import validate_tree, nodes_to_json
from collections import namedtuple

# Mock Node class for testing
Node = namedtuple('Node', ['id', 'label', 'content', 'parent_node_id'])

def test_nodes_to_json():
    nodes = [
        Node(id=1, label="Root", content="Content", parent_node_id=None),
        Node(id=2, label="Child 1", content="C1", parent_node_id=1),
        Node(id=3, label="Child 2", content="C2", parent_node_id=1),
        Node(id=4, label="Grandchild", content="GC", parent_node_id=2)
    ]
    
    tree = nodes_to_json(nodes)
    assert tree['label'] == "Root"
    assert len(tree['children']) == 2
    
    child1 = next(c for c in tree['children'] if c['label'] == "Child 1")
    assert len(child1['children']) == 1
    assert child1['children'][0]['label'] == "Grandchild"

# Tests for parsing removed as logic moved to frontend

def test_validate_tree_valid():
    tree = {"label": "Root", "children": []}
    assert validate_tree(tree) is True

def test_validate_tree_invalid():
    tree = {"label": "Root"} # Missing children
    assert validate_tree(tree) is False
