import hashlib

# -------------------------
# MERKLE TREE UTILS
# -------------------------

def hash_data(data: str):
    return hashlib.sha256(data.encode()).hexdigest()

def build_merkle_tree(leaves):
    """
    Builds a full Merkle Tree from a list of leaves.
    Returns the full tree as a list of levels.
    """
    if not leaves:
        return []
    
    tree = [leaves]
    while len(tree[-1]) > 1:
        level = tree[-1]
        new_level = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i+1] if i+1 < len(level) else left
            new_level.append(hash_data(left + right))
        tree.append(new_level)
    return tree

def get_merkle_proof(leaves, index):
    """
    Generates a proof for the leaf at the given index.
    A proof is a list of sibling hashes.
    """
    tree = build_merkle_tree(leaves)
    proof = []
    curr_index = index
    
    for level in tree[:-1]:
        sibling_index = curr_index + 1 if curr_index % 2 == 0 else curr_index - 1
        if sibling_index < len(level):
            proof.append(level[sibling_index])
        else:
            # If no sibling (odd number of nodes), the node is its own sibling in this implementation
            proof.append(level[curr_index])
        curr_index //= 2
    return proof

def verify_merkle_proof(leaf_hash, proof, root, index):
    """
    Verifies a Merkle Proof.
    """
    curr_hash = leaf_hash
    curr_index = index
    
    for sibling_hash in proof:
        if curr_index % 2 == 0:
            curr_hash = hash_data(curr_hash + sibling_hash)
        else:
            curr_hash = hash_data(sibling_hash + curr_hash)
        curr_index //= 2
        
    return curr_hash == root