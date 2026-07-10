#!/usr/bin/env python3

# This file is part of the Trezor project.
#
# Copyright (C) SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

from __future__ import annotations

import hashlib
import sys
from typing import TextIO

import click

from trezorlib._internal.slip26 import parse_label

# Artefact info and fingerprint: (model integer, purpose, 32-byte fingerprint).
ArtefactFingerprint = tuple[int, int, bytes]


def parse_fingerprints_file(f: TextIO) -> set[ArtefactFingerprint]:
    """Parse ``<label>: HEX`` lines (as produced by firmware-fingerprint.py) into
    ``(model, purpose, fingerprint)`` targets.

    Blank lines and comments starting with ``#`` are ignored.
    """
    result: set[ArtefactFingerprint] = set()
    for lineno, raw in enumerate(f.read().splitlines(), 1):
        line = raw.split("#", 1)[0].strip()  # drop comments
        if not line:
            continue

        label, sep, hex_fingerprint = line.partition(":")
        if not sep:
            raise ValueError(f"{f.name}:{lineno}: expected 'label: HEX', got {raw!r}")

        try:
            model, purpose = parse_label(label.strip())
        except ValueError as e:
            raise ValueError(f"{f.name}:{lineno}: {e}") from e

        try:
            # whitespace between hex digits is allowed, e.g. "1111 2222 ..."
            fingerprint = bytes.fromhex("".join(hex_fingerprint.split()))
        except ValueError:
            raise ValueError(f"{f.name}:{lineno}: invalid hex") from None

        if len(fingerprint) != 32:
            raise ValueError(
                f"{f.name}:{lineno}: fingerprint must be 32 bytes, got {len(fingerprint)}"
            )

        result.add((model, purpose, fingerprint))

    return result


def master_fingerprint(fingerprints: set[ArtefactFingerprint]) -> bytes:
    """Hash the targets into the master fingerprint, in canonical order."""
    if not fingerprints:
        raise ValueError("no fingerprints found")

    ctx = hashlib.sha256()
    for model, purpose, fingerprint in sorted(fingerprints):
        ctx.update(model.to_bytes(4, "little"))
        ctx.update(purpose.to_bytes(1, "little"))
        ctx.update(fingerprint)
    return ctx.digest()


@click.command()
@click.argument(
    "fingerprints_files",
    metavar="[FINGERPRINTS_FILE]...",
    nargs=-1,
    type=click.File("r"),
)
def firmware_master_fingerprint(fingerprints_files: tuple[TextIO, ...]) -> None:
    """Compute the master fingerprint from one or more fingerprints files.

    Each FINGERPRINTS_FILE holds '<label>: HEX' lines, as produced by
    firmware-fingerprint.py. When no file is given, stdin is read. Blank lines
    and comments starting with '#' are ignored. Model-agnostic objects that are
    not built here (e.g. definitions, translations) can be appended as
    'definitions: HEX' / 'translations: HEX' lines. The fingerprints are
    de-duplicated, sorted in canonical order, and hashed into the result.
    """
    if not fingerprints_files:
        fingerprints_files = (sys.stdin,)
    try:
        fingerprints: set[ArtefactFingerprint] = set()
        for f in fingerprints_files:
            fingerprints |= parse_fingerprints_file(f)
        master = master_fingerprint(fingerprints)
    except ValueError as e:
        raise click.ClickException(str(e)) from e

    click.echo(f"Master fingerprint: {master.hex(' ', 2)}")


if __name__ == "__main__":
    firmware_master_fingerprint()
