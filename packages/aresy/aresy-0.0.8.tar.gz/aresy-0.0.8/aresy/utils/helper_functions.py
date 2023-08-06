#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, numpy as np

def wrap_outputs_to_json(raw_outputs: dict = {"keys": [], "outputs": {}}) -> str:
    """helper function to wrap outputs into a pure python object
    and employ json dumps on it.
    """
    assert ( raw_outputs.get("keys", None) )
    assert ( raw_outputs.get("outputs", None) )

    keys = raw_outputs["keys"]
    pythonized_outputs = {}
    for k, o in raw_outputs["outputs"].items(): 
        if o is None: return None
        if isinstance(o, np.ndarray): o = o.tolist()
        pythonized_outputs[k] = o

    outputs = json.dumps({
            "keys": keys, 
            "outputs": pythonized_outputs
        }, ensure_ascii=False)
    return outputs

