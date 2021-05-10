import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    content = (f"{fmt} {str(len(data))}\0").encode() + data
    sha = hashlib.sha1(content).hexdigest()
    if write:
        gitdir = repo_find()
        head = sha[0:2]
        body = sha[2:] 
        path = pathlib.Path(gitdir / "objects" / head)
        if not path.is_dir():
            os.makedirs(path)
        pathlib.Path(path / body).touch()
        f = open(path / body, "wb")
        f.write(zlib.compress(content, -1))
        f.close()
    return sha


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if len(obj_name) < 4 or len(obj_name)>41:
        raise AssertionError(f"Not a valid object name {obj_name}")
    objs = []
    path = pathlib.Path(gitdir / "objects" / obj_name[0:2])
    for i in os.listdir(path):
        if i == obj_name[2:] or i[0:len(obj_name[2:])] == obj_name[2:]:
            objs.append(obj_name[0:2] + i)
    if len(objs) == 0:
        raise AssertionError(f"Not a valid object name {obj_name}")
    return objs


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    return resolve_object(obj_name, gitdir)[0]


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    obj = find_object(sha, gitdir)
    path = pathlib.Path(gitdir / "objects" / obj[0:2] / obj[2:])
    f = open(path, "rb")
    obj_data = zlib.decompress(f.read())
    data_len = int (obj_data[obj_data.find(b" ")+1:obj_data.find(b"\x00")])
    fmt = obj_data[:obj_data.find(b" ")].decode()
    data = obj_data[obj_data.find(b"\x00")+1:]
    f.close()
    return fmt, data


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    tree = []
    while len(data) > 0:
        start_index = data.find(b"\x00")
        fmt_code, fmt_name = data[:start_index].split(b" ")
        fmt_code = fmt_code.decode()
        fmt_name = fmt_name.decode()
        sha = data[start_index + 1 : start_index + 21]
        tree.append((int(fmt_code), fmt_name, sha.hex()))
        data = data[start_index + 21 :]
    return tree



def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find()
    fmt, data = read_object(obj_name, gitdir)
    if fmt == "blob":
        if pretty:
            print(data.decode())
        else:
            print(data)
        return
    elif fmt == "tree":
        for tree in read_tree(data):
            if tree[0] != 40000:
                print(f"{tree[0]:06}", "blob", tree[2] + "\t" + tree[1])
            else:
                print(f"{tree[0]:06}", "tree", tree[2] + "\t" + tree[1])
    else:
        print(data.decode())




def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    fmt, content = read_object(tree_sha, gitdir)
    objects = read_tree(content)
    result = []
    for i in objects:
        if i[0] == 100644 or i[0] == 100755:
            result.append((i[1], i[2]))
        else:
            sub_objects = find_tree_files(i[2], gitdir)
            for sub_obj in sub_objects:
                result.append((i[1] + "/" + sub_obj[0], sub_obj[1]))
    return result


def commit_parse(raw: bytes, start: int = 0, dct=None):
    pass
