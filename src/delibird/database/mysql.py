"""Mysql Connector helper"""


def dsn_to_args(dsn, args):
    """split mysql connect dsn to params dict"""
    slash_split = dsn.split("/")
    host_port = slash_split[2]
    db_others = slash_split[3]

    host_port_split = host_port.split(":")
    args["host"] = host_port_split[0]
    args["port"] = int(host_port_split[1])

    db_others_split = db_others.split("?")
    args["db"] = db_others_split[0]
    others = db_others_split[1]
    others_split = others.split("&")

    count = 0
    for other in others_split:
        other_split = other.split("=")
        key = other_split[0]
        if key == "user":
            args["user"] = other_split[1]
            count += 1
        elif key == "password":
            args["password"] = other_split[1]
            count += 1
        if count >= 2:
            break
