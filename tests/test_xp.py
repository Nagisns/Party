from pathlib import Path

import pytest

from cogs.leveling import _xp
from cogs.leveling._xp import XpRepository


@pytest.fixture(autouse=True)
def initialize_xp_database(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(_xp, "DB_FILE", tmp_path / "level.db")
    XpRepository.create()


def test_create_preserves_existing_xp() -> None:
    XpRepository.add_xp(guild_id=1, user_id=10, xp=10)

    XpRepository.create()

    assert XpRepository.get_user_xp(guild_id=1, user_id=10) == 10


def test_add_xp_returns_and_persists_running_total() -> None:
    assert XpRepository.add_xp(guild_id=1, user_id=10, xp=10) == 10
    assert XpRepository.add_xp(guild_id=1, user_id=10, xp=25) == 35

    assert XpRepository.get_user_xp(guild_id=1, user_id=10) == 35


def test_xp_is_scoped_to_guild_and_user() -> None:
    XpRepository.add_xp(guild_id=1, user_id=10, xp=10)
    XpRepository.add_xp(guild_id=1, user_id=20, xp=25)
    XpRepository.add_xp(guild_id=2, user_id=10, xp=75)

    assert XpRepository.get_user_xp(guild_id=1, user_id=10) == 10
    assert XpRepository.get_user_xp(guild_id=1, user_id=20) == 25
    assert XpRepository.get_user_xp(guild_id=2, user_id=10) == 75
    assert XpRepository.get_user_xp(guild_id=2, user_id=20) is None


def test_get_user_xp_distinguishes_missing_record_from_zero() -> None:
    assert XpRepository.get_user_xp(guild_id=1, user_id=10) is None

    XpRepository.add_xp(guild_id=1, user_id=10, xp=0)

    assert XpRepository.get_user_xp(guild_id=1, user_id=10) == 0
