import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    action_sha = commit_tree(gitdir, write_tree(gitdir, read_index(gitdir)), message, author=author)
    if is_detached(gitdir):
        ref = gitdir / "HEAD"
    else:
        ref = get_ref(gitdir)
    f = open(gitdir / ref, "w")
    f.write(action_sha)
    f.close()
    return action_sha

def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    ref = get_ref(gitdir)
    if os.path.isfile(gitdir/ref):
        f = pathlib.Path(gitdir/ref).open("r")
        ref = f.read()
        f.close()
    fmt, old_content = read_object(ref, gitdir)
    old_content = old_content.decode()
    tree_sha = old_content[5:45]
    old_objects = find_tree_files(tree_sha, gitdir)
    dirs = gitdir.absolute().parent
    for i in old_objects:
        os.remove(dirs / i[0])
        next_path = pathlib.Path(i[0]).parent 
        while len(next_path.parents) > 0:
            os.rmdir(next_path)
            next_path = pathlib.Path(next_path).parent
    f = pathlib.Path(gitdir / "HEAD").open("w")
    f.write(obj_name)
    f.close()    
    fmt, new_content = read_object(obj_name, gitdir)
    new_content = new_content.decode()
    new_tree_sha = new_content[5:45]
    new_objects = find_tree_files(new_tree_sha, gitdir)
    for i in new_objects:
        z = len(pathlib.Path(i[0]).parents)
        sub_path = dirs
        for sub in range(z - 2, -1, -1):
            sub_path /= pathlib.Path(i[0]).parents[sub]
            if not os.path.isdir(sub_path):
                os.mkdir(sub_path)
        fmt, obj_content = read_object(i[1], gitdir)
        if fmt == "blob":
            pathlib.Path(dirs / i[0]).touch()
            f = pathlib.Path(dirs / i[0]).open("w")
            f.write(obj_content.decode())
            f.close()
        else:
            os.mkdir(dirs / i[0])

