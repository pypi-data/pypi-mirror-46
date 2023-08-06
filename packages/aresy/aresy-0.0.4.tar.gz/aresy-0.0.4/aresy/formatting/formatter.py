#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, itertools, json, numpy as np

def get_tsv_headers(path: str) -> list:
    """helper function to get tsv file headers.
    """
    fd = open(path, "r")
    headers = fd.readline().replace("\n", "").split("\t")
    fd.close()
    return headers

class TSVPlaceholder(object):
    def __init__(self, names: list = [], name2index: dict = {}) -> None:
        """initialize a placeholder handler for tsv file. the params passed in are usually ignored.
        unless the file is broken, you may want to manually define these.
        """
        self.names = names
        self.name2index = name2index

    @classmethod
    def init_from_file(cls, path: str):
        """initialize the settings from file for later forward use.
        """
        names = get_tsv_headers(path)
        name2index= {n: i for i, n in enumerate(names)}
        return cls(names, name2index)

    def __call__(self, chunk: list):
        """forward the data into the placeholders.
        """
        assert (self.names)
        if self.names[0] in chunk[0]: return

        chunk = np.array( [entry.replace("\n", "").split("\t") for entry in chunk], dtype=object )

        source = {}
        for name in self.names:
            index = self.name2index.get(name, -1)
            if (index == -1): raise Exception("Wrong name2index mapping.")
            data = chunk[:, index].reshape(-1, 1)
            source[name] = data
        return source


class TSVDataLoader(object):
    def __init__(self, groupby: list, names: list = [], name2index: dict = {}, fd: int = None, hard_chunk_size: int = 1024000) -> None:
        """initialize an itertools groupby handler for tsv file. the params passed in are usually ignored.
        unless the file is broken, you may want to manually define these.
        """
        self.groupby = groupby
        self.names = names
        self.name2index = name2index
        self.hard_chunk_size = hard_chunk_size
        self.fd = fd

    @classmethod
    def init_from_file(cls, groupby: list, path: str, is_fdin: bool = True, encoding: str = "utf-8", hard_chunk_size: int = 1024000):
        """initialize the settings from file for later forward use.
        """
        names = get_tsv_headers(path)
        name2index= {n: i for i, n in enumerate(names)}
        fd = open(path, "r", encoding=encoding) if is_fdin else None
        return cls(groupby, names, name2index, fd, hard_chunk_size)

    def _groupby_func(self, line):
        """helper function as a groupby function.
        """
        indexes = [self.name2index.get(k, -1) for k in self.groupby]
        if (-1 in indexes): raise Exception("Wrong groupby keys.")

        line = line.replace("\n", "").split("\t")
        return [line[i] for i in indexes]

    def __call__(self, fdin: int = None):
        """build a data generator.
        """
        self.fd = fdin if fdin else self.fd
        assert (self.fd)
        for k, g in itertools.groupby(self.fd, key=self._groupby_func):
            chunk = []
            for i, e in enumerate(g):
                if i >= self.hard_chunk_size: 
                    print("Exceeds hard size. So skips to continue. The key is %s" % (str(k)))
                    break
                chunk.append(e)
            yield k, chunk

