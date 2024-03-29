import pytest

from randovania.game_description import data_reader
from randovania.layout.layout_description import LayoutDescription
from randovania.resolver import resolver, debug


@pytest.mark.skip_resolver_tests
def test_resolver_with_log_file(test_files_dir):
    # Setup
    debug.set_level(0)

    description = LayoutDescription.from_file(test_files_dir.joinpath("log_files", "seed_a.json"))
    configuration = description.permalink.presets[0].layout_configuration
    patches = description.all_patches[0]

    # Run
    final_state_by_resolve = resolver.resolve(configuration=configuration,
                                              patches=patches)

    # Assert
    assert final_state_by_resolve is not None
