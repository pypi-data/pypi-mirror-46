import sys
import json
import argparse
import traceback
from .yaml.YAMLDoc import YAMLDoc
from .utils import marshal_output


def main(args):
    cli_parser = argparse.ArgumentParser(
            description='configuration arguments provided at run time from the CLI'
        )
    cli_parser.add_argument(
        '-params',
        '--parameters',
        dest='params',
        type=json.loads,
        default="{}",
        help='cli parameters'
    )

    options, cli = cli_parser.parse_known_args(args)
    doc = YAMLDoc.open(cli[0], options.params)
    try:
        for expression in doc:
                print("********************************************************")
                print("*                %s" % expression[0])
                print("********************************************************")
                marshal_output(expression)
        if(len(cli) == 2):
            doc.save(cli[1])
    except Exception as e:
        print(e.__str__())
        raise
    finally:
        doc.close()


if __name__ == "__main__":
    main(sys.argv[1:])
    