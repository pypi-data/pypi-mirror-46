=============================
 Rezip - Repack ZIP Archives
=============================

Repack ZIP archives with the possibility to update metadata, e.g.,
Unix access right bits. Rezip can be used to fix Windows generated ZIP
archives (e.g., Python wheel packages) so that the archives members
have suitable access rights for usage on Linux.


GitLab page: https://gitlab.com/dfritzsche/python-rezip


Using rezip
===========


Usage::

   rezip [--inplace]
         [--glob|-g]
         [--normalize-access-rights] [--date-time DATETIME]
         [--output|-o OUTPUT]
         INPUT [INPUT]...

``--inplace``
   Repack in place. This is done by writing to a temporary file and
   then replace the original input file with the temporary output
   file. On Posix systems an atomic move is used for the replacement
   of the original input file by the temporary output file.

   More than one ``INPUT`` file can be specified if ``--inplace`` is
   used.

   Note: The ``--inplace`` option is mutual exclusive with the
   ``--output`` option.

``--glob | -g``
   Treat the input file names as shell glob patterns.

``--normalize-access-rights``
   Normalize the Unix access right bits. Access rights of regular
   non-executable files are modified to ``0o644``. Access rights of
   executable files are modified to be ``0o755``. Rezip considers
   files that already have any executable bit set and files that are
   identified as ELF programs or ELF dynamic libraries as executable.

   Identification as an ELF file is done by looking if the file starts
   with the ELF magic bytes ``b"\x7fELF"`` and then reading the
   `e_type` field of the ELF header. As this is in the end only a
   heuristic, wrong executable-identifcations may happen.

``--date-time DATETIME``
   Set the date time of all files in the ZIP archive to
   ``DATETIME``. The date time ``DATETIME`` must be a Unix timestamp
   or a date time in ISO format that is understood by
   `datetime.datetime.fromisoformat`.

``INPUT``
   The ZIP archive to read

   More than one ``INPUT`` file can be specified if ``--inplace`` is
   used. Otherwise, only one ``INPUT`` file is allowed.

``--output | -o``
   The ZIP archive to create and write to.

   Note: The ``--output`` option is mutual exclusive with the
   ``--inplace`` option.
