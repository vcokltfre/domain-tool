from json import dumps, loads
from pathlib import Path

from CloudFlare import CloudFlare

DIR = Path.home() / ".domaincfg"
DIR.mkdir(exist_ok=True, parents=True)

TOKEN, EMAIL = (DIR / "cred").read_text().strip().split("\n")

CONF = DIR / "config.json"
if not CONF.exists():
    CONF.write_text(dumps({}))

CLIENT = CloudFlare(EMAIL, TOKEN)
ZONE_MAP: dict[str, str] = loads(CONF.read_text())


def refresh_zones():
    for zone in CLIENT.zones.get(params={"per_page": 50}):  # type: ignore
        ZONE_MAP[zone["name"]] = zone["id"]  # type: ignore

    CONF.write_text(dumps(ZONE_MAP))


if not ZONE_MAP:
    refresh_zones()
