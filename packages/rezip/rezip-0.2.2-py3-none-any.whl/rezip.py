#!/usr/bin/env python3
"""Repack a ZIP file
"""
# pylint: disable=invalid-name,redefined-builtin
import argparse
import os
import stat
import struct
import sys

from typing import BinaryIO, Callable, Optional, Tuple, cast
from zipfile import ZipFile, ZipInfo


__version__ = "0.2.2"


class Arguments:
    """Data holder for program arguments"""
    inplace: bool = False
    normalize_access_rights = False
    input: str = ""
    output: str = ""
    verbosity: int = 1

    def __str__(self) -> str:
        cls_name = self.__class__.__name__
        args = []
        for key, val in self.__dict__.items():
            args.append(f"{key}={val!r}")
        return f"{cls_name}({', '.join(args)})"


FilterFunc = Callable[[ZipInfo, bytes], Optional[Tuple[ZipInfo, bytes]]]


def parse_args(argv=None) -> Arguments:
    """Parse rezip arguments"""
    if argv is None:
        argv = sys.argv
    p = argparse.ArgumentParser()
    p.add_argument("--quiet", "-q", dest="verbosity", action="store_const", const=0,
                   help="Produce less output")
    p.add_argument("--verbose", "-v", dest="verbosity", action="count", default=1,
                   help="Be more verbose")
    p.add_argument("--inplace", action="store_true", default=False,
                   help="Repack in place")
    p.add_argument("--normalize-access-rights", action="store_true",
                   default=False,
                   help="Normalize Unix access rights")
    p.add_argument("input", help="Name of the wheel file to repack")
    p.add_argument("output", nargs="?", default="",
                   help="Name of the output file")
    args = cast(Arguments, p.parse_args(argv[1:], namespace=Arguments()))
    if args.inplace:
        if args.output:
            p.error("argument output invalid if used together with argument --inplace")
        args.output = f"{args.input}.tmp"
        if os.path.exists(args.output):
            p.error("internal error: {args.output} exists")
    else:
        if not args.output:
            p.error("argument output is missing (use --inplace for inplace repack)")
        if args.input == args.output:
            p.error("arguments input and output are equal (use --inplace for inplace repack)")
    return args


def rezip(infile: BinaryIO,
          outfile: BinaryIO,
          filter: Optional[FilterFunc] = None) -> None:
    """Repack contents of *infile* to *outfile*.

    :arg BinaryIO infile: Input ZIP file
    :arg BinaryIO outfile: Output ZIP file
    :arg Optional[FilterFunc] filter: Filter function to modify or
        update ZIP file members

    If given, the callable *filter* is used to map input members to
    output members. For each member in the input ZipFile *filter* is
    called with the :class:`~zipfile.ZipInfo` object and the bytes of
    the member. It must return a tuple containing the
    :class:`~zipfile.ZipInfo` object and the bytes to write to
    *outfile*.  So, *filter* could be used to change the file name,
    UNIX access rights or the contents of a ZipFile member.  If
    *filter* returns `None` then the member will be skipped and not
    written to *outfile*. *filter* is allowed to modify its input
    arguments and return the modified arguments.

    """
    with ZipFile(infile, mode="r") as zin:
        with ZipFile(outfile, mode="w") as zout:
            for zinfo in zin.infolist():
                data = zin.read(zinfo.filename)
                if filter:
                    zinfo_data = filter(zinfo, data)
                    if zinfo_data is None:
                        # Skip the current member
                        continue
                    zinfo, data = zinfo_data
                zout.writestr(zinfo, data)



def data_is_executable(data: bytes) -> bool:
    """Check if *data* is likely an executable

    Note: For now, *data* is only checked for looking like an ELF
    executable or shared library.

    """
    if len(data) >= 52 and data[:0x04] == b"\x7fELF":
        # Looks like an ELF header, check e_type
        endianness_flag_int = data[0x05]
        e_type_bytes = data[0x10:0x12]
        fmt = "<h" if endianness_flag_int == 1 else ">h"
        e_type = struct.unpack(fmt, e_type_bytes)[0]
        # ET_EXEC = 0x02 (e.g., static linked programs or non-pie programs)
        # ET_DYN = 0x03 (e.g., shared libraries or pie programs)
        return e_type in (0x02, 0x03)
    else:
        return False


class NormalizeAccessRightsFilter:

    def __init__(self, args: Arguments) -> None:
        self.args = args

    def __call__(self, zinfo: ZipInfo, data: bytes) -> Tuple[ZipInfo, bytes]:
        """Normalize Unix access rights"""
        filemode = old_filemode = zinfo.external_attr >> 16

        if stat.S_ISREG(old_filemode):
            if (old_filemode & 0o111 != 0) or data_is_executable(data):
                access_rights = 0o755
            else:
                access_rights = 0o644

            filemode = (filemode & ~0o777) | access_rights
            zinfo.external_attr &= 0xffff
            zinfo.external_attr |= (filemode << 16)

        if old_filemode != filemode or (filemode & 0o111 != 0):
            if self.args.verbosity > 0:
                print("%s: %06o -> %06o" % (zinfo.filename, old_filemode, filemode))

        return zinfo, data


def main(argv=None):
    """ReZip Main program"""
    args = parse_args(argv)
    if args.verbosity > 1:
        print(f"Read ZIP file {args.input}")
    with open(args.input, mode="rb") as fin:
        if args.verbosity > 1:
            print(f"Write ZIP file {args.output}")
        with open(args.output, mode="wb") as fout:
            filter_func: Optional[FilterFunc]
            if args.normalize_access_rights:
                filter_func = NormalizeAccessRightsFilter(args)
            else:
                filter_func = None
            rezip(fin, fout, filter_func)
    if args.inplace:
        os.replace(args.output, args.input)


if __name__ == "__main__":
    sys.exit(main())
