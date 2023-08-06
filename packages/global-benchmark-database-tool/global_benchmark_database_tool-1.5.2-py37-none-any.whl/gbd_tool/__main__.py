import sys

from main.gbd_tool.config_manager import make_standard_configuration


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    print("||Installing config data||\n")
    make_standard_configuration()
    print("||done||\n")


if __name__ == "__main__":
    main()
