"""
Functions for parsing PIREPs
"""

from avwx import _core, static, structs
from avwx.exceptions import BadStation
from avwx.structs import (
    Aircraft,
    Cloud,
    Icing,
    Location,
    Number,
    PirepData,
    Timestamp,
    Turbulance,
    Units,
)

_units = Units(**static.NA_UNITS)


def _root(item: str) -> dict:
    """
    Parses report root data including station and report type
    """
    items = item.split()
    rtype = None
    station = None
    # Find valid station
    for item in items:
        try:
            _core.valid_station(item)
            station = item
            break
        except BadStation:
            continue
    # Determine report type
    if "UA" in items:
        rtype = "UA"
    elif "UUA" in items:
        rtype = "UUA"
    return {"station": station, "type": rtype}


def _location(item: str) -> Location:
    """
    Convert a location element to a Location object
    """
    items = item.split()
    if not items:
        return
    station, direction, distance = None, None, None
    if len(items) == 1:
        ilen = len(item)
        # MLB
        if ilen < 5:
            station = item
        # MKK360002 or KLGA220015
        elif ilen in (9, 10) and item[-6:].isdigit():
            station, direction, distance = item[:-6], item[-6:-3], item[-3:]
    # 10 WGON
    elif items[0].isdigit():
        station, direction, distance = items[1][-3:], items[1][:-3], items[0]
    # GON 270010
    elif items[1].isdigit():
        station, direction, distance = items[0], items[1][:3], items[1][3:]
    # Convert non-null elements
    if direction:
        direction = _core.make_number(direction)
    if distance:
        distance = _core.make_number(distance)
    return Location(item, station, direction, distance)


def _time(item: str) -> Timestamp:
    """
    Convert a time element to a Timestamp
    """
    return _core.make_timestamp(item, time_only=True)


def _altitude(item: str) -> "Number|str":
    """
    Convert reporting altitude to a Number or string
    """
    if item.isdigit():
        return _core.make_number(item)
    return item


def _aircraft(item: str) -> str:
    """
    Returns the Aircraft from the ICAO code
    """
    try:
        return Aircraft.from_icao(item)
    except ValueError:
        return item


def _clouds(item: str) -> [Cloud]:
    """
    Convert cloud element to a list of Clouds
    """
    clouds = item.split()
    # BASES 004 TOPS 016
    if "BASES" in clouds and "TOPS" in clouds:
        base = clouds[clouds.index("BASES") + 1]
        top = clouds[clouds.index("TOPS") + 1]
        return [structs.Cloud(item, base=base, top=top)]
    return [_core.make_cloud(cloud) for cloud in clouds]


def _number(item: str) -> Number:
    """
    Convert an element to a Number
    """
    return _core.make_number(item)


def _turbulance(item: str) -> Turbulance:
    """
    Convert reported turbulance to a Turbulance object
    """
    items = item.split()
    ret = {"severity": None, "floor": None, "ceiling": None}
    for i, item in enumerate(items):
        hloc = item.find("-")
        if hloc > -1 and item[:hloc].isdigit() and item[hloc + 1 :].isdigit():
            for key, val in zip(("floor", "ceiling"), items.pop(i).split("-")):
                ret[key] = _core.make_number(val)
            break
    ret["severity"] = " ".join(items)
    return Turbulance(**ret)


def _icing(item: str) -> Icing:
    """
    Convert reported icing to an Icing object
    """
    items = item.split()
    ret = {"severity": items.pop(0), "type": None, "floor": None, "ceiling": None}
    for i, item in enumerate(items):
        hloc = item.find("-")
        if hloc > -1 and item[:hloc].isdigit() and item[hloc + 1 :].isdigit():
            for key, val in zip(("floor", "ceiling"), items.pop(i).split("-")):
                ret[key] = _core.make_number(val)
            break
    if items:
        ret["type"] = items[0]
    return Icing(**ret)


def _remarks(item: str) -> str:
    """
    Returns the remarks. Reserved for later parsing
    """
    return item


def _wx(item: str) -> dict:
    """
    Parses remaining weather elements
    """
    ret = {"wx": []}
    items = item.split()
    for item in items:
        if len(item) < 3:
            ret["wx"].append(item)
        elif item.startswith("FV"):
            _, ret["flight_visibility"] = _core.get_visibility([item[2:]], _units)
        else:
            ret["wx"].append(item)
    return ret


_handlers = {
    "OV": ("location", _location),
    "TM": ("time", _time),
    "FL": ("altitude", _altitude),
    "TP": ("aircraft", _aircraft),
    "SK": ("clouds", _clouds),
    "TA": ("temperature", _number),
    "TB": ("turbulance", _turbulance),
    "IC": ("icing", _icing),
    "RM": ("remarks", _remarks),
}


_dict_handlers = {"WX": _wx}


def parse(report: str) -> PirepData:
    """
    Returns a PirepData object based on the given report
    """
    if not report:
        return None
    clean = _core.sanitize_report_string(report)
    wxdata, *_ = _core.sanitize_report_list(clean.split())
    sanitized = " ".join(wxdata)
    wxresp = {"raw": report, "sanitized": sanitized, "station": None, "remarks": None}
    wxdata = sanitized.split("/")
    wxresp.update(_root(wxdata.pop(0).strip()))
    for item in wxdata:
        if not item or len(item) < 2:
            continue
        tag = item[:2]
        item = item[2:].strip()
        if tag in _handlers:
            key, handler = _handlers[tag]
            wxresp[key] = handler(item)
        elif tag in _dict_handlers:
            wxresp.update(_dict_handlers[tag](item))
    return PirepData(**wxresp)
