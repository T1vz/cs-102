import pathlib
import typing as tp

def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    pathlib.Path(gitdir / ref).touch()
    f = open(gitdir / ref, "w")
    f.write(new_value)
    f.close()


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    pass


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD":
        refname = get_ref(gitdir)
    path = gitdir / refname
    if not path.exists():
        return None
    f = open(path, "r")
    contents = f.read()
    f.close()
    return contents


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, "HEAD")


def is_detached(gitdir: pathlib.Path) -> bool:
    f = open(gitdir / "HEAD", "r")
    com = f.read()
    f.close()
    if len(com) == 40 and com[:5] != "ref: ":
        return True
    else:
        return False

def get_ref(gitdir: pathlib.Path) -> str:
    f = open(gitdir / "HEAD", "r")
    ref = f.read()
    if ref[:5] == 'ref: ':
        ref = ref[5:-1] 
    f.close()
    return ref