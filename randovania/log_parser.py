import typing
import re
from enum import Enum

RANDOMIZER_VERSION = "3.2"


class Game(Enum):
    PRIME2 = "prime2"


class PickupEntry(typing.NamedTuple):
    world: str
    room: str
    item: str


class RandomizerLog(typing.NamedTuple):
    version: str
    seed: str
    excluded_pickups: str
    pickup_entries: typing.List[PickupEntry]


class InvalidLogFileException(Exception):
    def __init__(self, logfile, reason):
        super().__init__("File '{}' is not a valid Randomizer log: {}".format(logfile, reason))


class UnknownGameException(Exception):
    pass


def extract_with_regexp(logfile, f, regex, invalid_reason):
    match = re.match(regex, f.readline().strip())
    if match:
        return match.group(1)
    else:
        raise InvalidLogFileException(logfile, invalid_reason)


def parse_log(logfile: str) -> RandomizerLog:
    with open(logfile) as f:
        version = extract_with_regexp(logfile, f, r"Randomizer V(\d+\.\d+)", "Could not find Randomizer version")
        if version != RANDOMIZER_VERSION:
            raise InvalidLogFileException(logfile, "Unexpected version {}, expected {}".format(version,
                                                                                               RANDOMIZER_VERSION))

        seed = extract_with_regexp(logfile, f, r"^Seed: (\d+)$", "Could not find Seed")
        excluded_pickups = extract_with_regexp(logfile, f, r"^Excluded pickups: (\d+)$",
                                               "Could not find excluded pickups")

        pickups = []
        for line in f:
            m = re.match(r"^([^-]+)(?:\s-)+([^-]+)(?:\s-)+([^-]+)$", line)
            if m:
                pickups.append(PickupEntry(*map(str.strip, m.group(1, 2, 3))))

        return RandomizerLog(version, seed, excluded_pickups, pickups)


prime2_worlds = {
    "Temple Grounds",
}


def resolve_game_argument(game: str, log: RandomizerLog) -> Game:
    if game != "auto":
        return Game(game)

    if log.pickup_entries[0].world == "Temple Grounds":
        return Game.PRIME2

    raise UnknownGameException("Could not decide the game based on this logfile.")


def generate_game_choices() -> typing.List[str]:
    return [game.name.lower() for game in Game] + ["auto"]