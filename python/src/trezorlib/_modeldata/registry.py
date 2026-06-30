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

"""Aggregated registry of all model definitions (PROTOTYPE).

Once the firmware-side generator exists, the import list below is the only
thing it needs to emit/maintain (one line per ``core/embed/models/<NAME>``)."""

from __future__ import annotations

from typing import Dict, Optional, Tuple

from . import ModelData
from .D001 import MODEL as D001
from .D002 import MODEL as D002
from .D003 import MODEL as D003
from .T1B1 import MODEL as T1B1
from .T2B1 import MODEL as T2B1
from .T2T1 import MODEL as T2T1
from .T3B1 import MODEL as T3B1
from .T3T1 import MODEL as T3T1
from .T3T2 import MODEL as T3T2
from .T3W1 import MODEL as T3W1

ALL: Tuple[ModelData, ...] = (
    T1B1,
    T2T1,
    T2B1,
    T3T1,
    T3T2,
    T3B1,
    T3W1,
    D001,
    D002,
    D003,
)

BY_INTERNAL_NAME: Dict[str, ModelData] = {m.internal_name: m for m in ALL}


def by_internal_name(internal_name: str) -> Optional[ModelData]:
    return BY_INTERNAL_NAME.get(internal_name)
