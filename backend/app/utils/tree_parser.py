# parse_indented_text removed as parsing is now handled by frontend

def validate_tree(tree: dict) -> bool:
    """
    Validates that the tree has the required structure.
    """
    if not isinstance(tree, dict):
        return False
    if "label" not in tree or "children" not in tree:
        return False
    if not isinstance(tree["children"], list):
        return False
    
    for child in tree["children"]:
        if not validate_tree(child):
            return False
            
    return True

def nodes_to_json(nodes: list) -> dict:
    """
    Converts a flat list of Node objects (with parent_node_id) into a nested dictionary.
    Assumes a single root node exists in the list.
    """
    if not nodes:
        return None
        
    # Create a map of id -> node_dict
    node_map = {}
    for node in nodes:
        node_map[node.id] = {
            "id": node.id,
            "label": node.label,
            "content": node.content,
            "children": []
        }
    
    root = None
    
    for node in nodes:
        current = node_map[node.id]
        if node.parent_node_id is None:
            root = current
        else:
            parent = node_map.get(node.parent_node_id)
            if parent:
                parent["children"].append(current)
                
    return root
