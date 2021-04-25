import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    if "GIT_DIR" in os.environ:
        caption = pathlib.Path(os.environ["GIT_DIR"])

def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    # direct = workdir / pathlib.Path(os.environ["GIT_DIR"])
    if os.path.isfile(workdir):
        raise AssertionError(f"{workdir} is not a directory")
    direct = workdir / pathlib.Path(".git")
    if "GIT_DIR" in os.environ:
        direct = workdir / pathlib.Path(os.environ["GIT_DIR"])
    os.mkdir(direct)
    os.makedirs(os.path.join(direct, "refs", "heads"))
    os.mkdir(os.path.join(direct, "refs", "tags"))
    os.mkdir(os.path.join(direct, "objects"))
    pathlib.Path(os.path.join(direct, "HEAD")).touch()
    f = open(os.path.join(direct, "HEAD"), "w")
    f.write("ref: refs/heads/master\n")
    f.close()
    pathlib.Path(os.path.join(direct, "config")).touch()
    f = open(os.path.join(direct, "config"), "w")
    f.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
    f.close()
    pathlib.Path(os.path.join(direct, "description")).touch()
    f = open(os.path.join(direct, "description"), "w")
    f.write("Unnamed pyvcs repository.\n")
    f.close()
    return direct