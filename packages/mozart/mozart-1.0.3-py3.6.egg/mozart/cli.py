import argparse
import sys
from .__version__ import __version__
import logging
from mozart.music import get_music_handler, music_map


def main(origin_args):
    """
    command line program
    """

    parser = argparse.ArgumentParser(
        description="mozart - ♪ Nice API for developers who like musics",
        usage="python -m mozart [-h] [-v] [-l LINK] [-n NAME] [-m MUSIC_ID]"
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version='%(prog)s - version {}'.format(__version__))
    parser.add_argument(
        "-l", "--link", dest='link', type=str, default="",
        help='print out all info about this music from link.')
    parser.add_argument(
        "-n", "--name", dest='name', type=str, default="",
        help='name of music site. avaliable are: {}'.format(', '.join(music_map.keys())))
    parser.add_argument(
        "-m", "--music", dest='music_id', type=str, default="",
        help='print out all info about this music from music id.')
    args = parser.parse_args(origin_args)

    if args.name not in ["qq", "xiami", "netease"] or (not args.link and not args.music_id):
        parser.print_help()
        return -1

    # init logger
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)-8s | %(name)s: %(msg)s ",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("mozart")

    try:
        got, handler = get_music_handler(args.name)
        # main proccess
        if args.music_id:
            logger.debug("use music id to request")
            if got:
                handler(music_id=args.music_id, use_id=True)
        elif args.link:
            logger.debug("use link to request")
            if got:
                handler(url=args.link, use_id=False)
    except SystemExit:
        logger.info('exiting...')
        sys.exit(0)

    return 0


def app_main():
    sys.exit(main(sys.argv[1:]))
