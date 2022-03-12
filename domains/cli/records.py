from typing import Optional

from typer import Typer, echo

from ..impl import CLIENT, ZONE_MAP, refresh_zones

app = Typer()


@app.command(name="set")
def set(
    domain: str,
    name: str,
    content: str,
    type: str = "A",
    proxy: bool = True,
) -> None:
    CLIENT.zones.dns_records.post(
        ZONE_MAP[domain],
        data={
            "name": name,
            "content": content,
            "type": type,
            "proxied": proxy,
        },
    )

    echo(f"Set [{type}] {name} to {content} for {domain}")


@app.command(name="delete")
def delete(domain: str, name: str, type: Optional[str] = None) -> None:
    records = CLIENT.zones.dns_records.get(ZONE_MAP[domain])
    done = False

    for record in records:
        print(record)
        if record["name"] == f"{name}.{domain}" and (
            record["type"] == type if type else True
        ):
            CLIENT.zones.dns_records.delete(ZONE_MAP[domain], record["id"])

            echo(f"Deleted {name} for {domain}")
            done = True

    if not done:
        echo(f"No record found for {name} for {domain} to delete")


@app.command(name="list")
def list(filter: str = "") -> None:
    for name, id in ZONE_MAP.items():
        if not filter in name:
            continue

        print(f"[{id}] {name}")


@app.command(name="refresh")
def refresh() -> None:
    refresh_zones()
