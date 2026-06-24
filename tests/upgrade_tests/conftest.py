import logging
import tempfile
from pathlib import Path
from typing import Any, Generator

import pytest

from trezorlib._internal.emulator import TropicModel

from ..emulators import (
    TROPIC_MODEL_CONFIGFILE,
    delete_profile,
    get_logfile,
    is_tropic_capable_model,
)

LOG = logging.getLogger(__name__)


# This fixture is very similar to `tropic_model` from the parent directory, but has a "function"
# scope instead of session.
# We could save the time it takes to always stop and start the tropic model by using
# session-scoped instance but we'd need to somehow reset/wipe it after every test function.
@pytest.fixture
def shared_profile_dir(request) -> Generator[str, Any, Any]:
    # Use the default port because before 2.9.4 it was not configurable.
    # This means upgrade tests currently can't run in multiple threads for T3W1.
    tropic_model_port = 28992
    model = request.node.callspec.params["model"]
    start_tropic_model = is_tropic_capable_model(model)

    profile_dir = tempfile.TemporaryDirectory(
        prefix="trezor-upgrade-", delete=delete_profile()
    )
    LOG.debug(
        f"Test profile dir: {profile_dir.name} (delete: {delete_profile()}), start_tropic: {start_tropic_model}"
    )

    with profile_dir as path:
        # do not start tropic model when not supported
        if not start_tropic_model:
            yield path
            return

        with TropicModel(
            profile_dir=path,
            configfile=TROPIC_MODEL_CONFIGFILE,
            port=tropic_model_port,
            logfile=get_logfile("trezor-tropic-model.log", Path(profile_dir.name)),
        ) as tropic_model:
            tropic_model.start()
            yield path
