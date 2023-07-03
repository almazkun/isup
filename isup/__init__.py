import argparse
import logging
import os
import sys

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"))


def check(args):
    from .check import check_list

    print(check_list(args.url_list))


def main():
    parser = argparse.ArgumentParser(
        description="down-issue: if down(url): create_issue(github)"
    )

    subparsers = parser.add_subparsers(help="sub-command help")

    parser_check = subparsers.add_parser("check", help="check help")
    parser_check.add_argument("-u", "--url-list", nargs="+", help="url list to check")
    parser_check.set_defaults(func=check)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
