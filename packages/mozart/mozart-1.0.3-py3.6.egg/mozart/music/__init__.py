from .qq import QQ
from .netease import Netease
from .xiami import XiaMi

music_map = {
    "qq": QQ,
    "xiami": XiaMi,
    "netease": Netease
}


def get_music_handler(origin):
    """
    Get music handler from origin
    :param origin:
    :return: whether find it
    """
    if origin in music_map:
        return True, music_map[origin]
    else:
        return False, None


__all__ = ["get_music_handler", "music_map",
           "QQ", "XiaMi", "Netease"]
