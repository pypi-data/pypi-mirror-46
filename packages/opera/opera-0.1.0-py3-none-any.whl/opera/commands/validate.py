import argparse

import yaml

from opera import stdlib, types


def add_parser(subparsers):
    parser = subparsers.add_parser("validate", help="CSAR to validate")
    parser.add_argument("csar",
                        type=argparse.FileType("r"),
                        help="cloud service archive file")
    parser.set_defaults(func=validate)


def validate(args):
    print("Loading service template ...")
    service_template = types.ServiceTemplate.from_data(stdlib.load())
    service_template.merge(
        types.ServiceTemplate.from_data(yaml.safe_load(args.csar))
    )

    print("Resolving service template links ...")
    service_template.resolve()

    print("Done.")

    return 0

