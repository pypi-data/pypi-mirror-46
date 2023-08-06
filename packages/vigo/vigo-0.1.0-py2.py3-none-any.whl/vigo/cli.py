import argparse


def argparser(groups):
    parser = argparse.ArgumentParser(
        description="Search code in the given openstack group"
    )
    parser.add_argument(
        "query",
        help="your query on groups projects."
        "Based on github code search qualifiers "
        "(cf. https://help.github.com/en/articles/searching-code)",
    )
    parser.add_argument(
        "groups",
        nargs="+",
        help="Openstack groups to analyze.",
        choices=groups,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Only display the vigo version number",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Set the output verbose"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Set the debug mode"
    )
    return parser
