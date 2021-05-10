import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    line = b""
    for entry in index:
        if "/" in entry.name:
            line+=b"40000 "
            subdir = b""
            name_index = entry.name.find("/")
            dir_name = entry.name[: name_index]
            line += dir_name.encode() + b"\0"
            subdir += oct(entry.mode)[2:].encode() + b" "
            subdir += entry.name[name_index+1:].encode() + b"\0"
            subdir += entry.sha1
            blob_hash = hash_object(subdir, fmt ="tree", write=True)
            line += bytes.fromhex(blob_hash)
        else:
            line += oct(entry.mode)[2:].encode() + b" "
            line += entry.name.encode() + b"\0"
            line += entry.sha1
    return hash_object(line, fmt="tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if author is None and "GIT_AUTHOR_NAME" in os.environ and "GIT_AUTHOR_EMAIL" in os.environ:
        author = (
            os.getenv("GIT_AUTHOR_NAME", None) 
            + " "  
            + f'<{os.getenv("GIT_AUTHOR_EMAIL", None)}>'  
        )  
    if time.timezone > 0:
        timezone = "-"
    else:
        timezone = "+"
    timezone += f"{abs(time.timezone) // 60 // 60:02}{abs(time.timezone) // 60 % 60:02}"
    data = [f"tree {tree}"]
    if parent is not None:
        data.append(f"parent {parent}")
    data.append(f"author {author} {int(time.mktime(time.localtime()))} {timezone}")
    data.append(f"committer {author} {int(time.mktime(time.localtime()))} {timezone}")
    data.append(f"\n{message}\n")
    return hash_object("\n".join(data).encode(), "commit", write=True)