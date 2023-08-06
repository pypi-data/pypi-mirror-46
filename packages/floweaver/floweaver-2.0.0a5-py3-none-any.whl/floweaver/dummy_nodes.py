from .ordering import new_node_indices
from .sankey_definition import Waypoint


def add_dummy_nodes(G, v, w, bundle_key, node_kwargs=None, dummy_key=None):
    """Add edges to the graph with "dummy nodes" in every rank.

    So if the source `v` is in rank 0, and the target `w` is in rank 2, there
    will be a "dummy node" in rank 1 created, and two separate edges: (v ->
    dummy) and (dummy -> w). More complicated rules apply when the directions
    of `v` and `w` change.

    Args:
        G (LayeredGraph): The graph to begin with.
        v (str): The id of the source node.
        w (str): The id of the target node.
        bundle_key (int): The id of the bundle this link comes from.
        node_kwargs (dict): kwargs passed to the new Waypoint.
        dummy_key (str):
            Key to distinguish which links should share dummy nodes. Default:
            '{v}_{w}'.

    Returns:
        LayeredGraph: a copy of G with the nodes and edges added.

    """

    if node_kwargs is None:
        node_kwargs = {}

    if dummy_key is None:
        dummy_key = '{}_{}'.format(v, w)

    V = G.get_node(v)
    W = G.get_node(w)
    H = G.copy()
    rv, iv, jv = H.ordering.indices(v)
    rw, iw, jw = H.ordering.indices(w)

    if rw > rv:
        p = rv if V.direction == 'L' else rv + 1
        q = rw if W.direction == 'L' else rw - 1
        new_ranks = list(range(p, q + 1))
        d = 'R'
    elif rv > rw:
        p = rv if V.direction == 'R' else rv - 1
        q = rw if W.direction == 'R' else rw + 1
        new_ranks = list(range(p, q - 1, -1))
        d = 'L'
    else:
        new_ranks = []

    if not new_ranks:
        _add_edge(H, v, w, bundle_key)
        return H

    u = v
    for r in new_ranks:
        idr = '__{}_{}'.format(dummy_key, r)
        # Only add and position dummy nodes the first time -- bundles can share
        # a dummy node leading to this happening more than once
        if idr not in H.node:
            _add_edge(H, u, idr, bundle_key)
            if r == rv:
                i, j = iv, jv + (+1 if V.direction == 'R' else -1)
            else:
                prev_rank = H.ordering.layers[r + 1 if d == 'L' else r - 1]
                i, j = new_node_indices(H,
                                        H.ordering.layers[r],
                                        prev_rank,
                                        idr,
                                        side='below' if d == 'L' else 'above')
            H.ordering = H.ordering.insert(r, i, j, idr)
            H.add_node(idr, node=Waypoint(direction=d, **node_kwargs))
        else:
            _add_edge(H, u, idr, bundle_key)
        u = idr
    _add_edge(H, u, w, bundle_key)

    return H


def _add_edge(G, v, w, bundle_key):
    if G.has_edge(v, w):
        G[v][w]['bundles'].append(bundle_key)
    else:
        G.add_edge(v, w, bundles=[bundle_key])
