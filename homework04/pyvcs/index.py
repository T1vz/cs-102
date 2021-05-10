import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        data = (self.ctime_s, self.ctime_n, self.mtime_s,
                       self.mtime_n, self.dev, self.ino,
                       self.mode, self.uid, self.gid,
                       self.size, self.sha1, self.flags)
        name = self.name.encode('utf-8')
        return struct.pack(
            f">10i20sh{len(name) + 3}s",
            *data,
            name,
        )

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        (
            ctime_s,
            ctime_n,
            mtime_s,
            mtime_n,
            dev,
            ino,
            mode,
            uid,
            gid,
            size,
            sha1,
            flags,
        ) = struct.unpack(">10i20sh", data[:62])
        data = data[62:]
        last = data.find(b"\x00\x00\x00")
        name = data[:last].decode()
        return GitIndexEntry(
            ctime_s, ctime_n, mtime_s, mtime_n, dev, ino, mode, uid, gid, size, sha1, flags, name
        )


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    gitdir=pathlib.Path(gitdir/"index")
    if not pathlib.Path(gitdir).exists():
        return []
    else:
        f = open(gitdir, "rb")
        data = f.read()
        f.close()

        result = []

        gitIndex = struct.unpack(">4s2i", data[:12])
        data = data[12:]
        for i in range(gitIndex[2]):
            result.append(GitIndexEntry.unpack(data))
            data = data[62:]
            next_byte = data.find(b"\x00\x00\x00")
            data = data[next_byte + 3 :]
        return result




def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    result = []
    result.append(b"DIRC")
    result.append(struct.pack(">2i", 2, len(entries)))
    for entry in entries:
        result.append(entry.pack())
    path = pathlib.Path(gitdir / "index")
    data = b"".join(result)
    result.append(struct.pack(">20s", hashlib.sha1(data).digest()))
    path.touch()
    f = open(path, "wb")
    f.write(b"".join(result))
    f.close()


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    data = read_index(gitdir)
    result = []
    if details:
        for i in data:
            if i.mode == 33188:
                result.append(" ".join(['100644', str(i.sha1.hex()), "0"])+"\t" + i.name+"\n")
            else:
                result.append(" ".join(['100755', str(i.sha1.hex()), "0"])+"\t" + i.name+"\n")
        print("".join(result))
    else:
        for i in data:
            result.append(i.name+"\n")
        print("".join(result))


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    if not os.path.isfile(gitdir / "index"):
        pathlib.Path(gitdir / "index").touch()
        entries = []
    else:
        entries = read_index(gitdir)
    for i in paths:
        f = open(i, 'r')
        data = f.read()
        f.close()
        sha = hashlib.sha1((f"blob {len(data)}\0" + data).encode())
        data = data.encode()
        path = hash_object(data, "blob", True)
        new_path = str(i).replace("\\", "/")
        info = os.stat(i)
        if len(new_path) > 7:
            flag = 7
        else:
            flag = len(new_path)
        gie = GitIndexEntry(ctime_s = int(info[9]),
            ctime_n = 0,
            mtime_s = int(info[8]),
            mtime_n = 0,
            dev = int(info[2]),
            ino = int(info[1]),
            mode = int(info[0]),
            uid = int(info[4]),
            gid = int(info[5]),
            size = int(info[6]),
            sha1 = sha.digest(),
            flags = flag,
            name = new_path
            )
        entries.append(gie)
    entries.sort(key=lambda x: x.name)
    write_index(gitdir, entries)