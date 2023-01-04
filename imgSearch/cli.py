from engine import Engine
import argparse
import os

def parseArgs() -> dict[str, any]:
    """Parces arguments passed via cli, performs error checking, and returns arg dict.

    :raises SystemExit: PathNotFound
    :raises SystemExit: PathNotDirectory
    :return: dictionary containing args
    :rtype: dict[str, any]
    """    
    parser = argparse.ArgumentParser(prog="imgSearch", description="Local Image Search Utility")

    parser.add_argument("-a", "--add")
    parser.add_argument("-s", "--search")
    parser.add_argument("-i", "--info", action="store_true")
    args = vars(parser.parse_args())

    if args["add"] and not os.path.exists(args["add"]):
        raise SystemExit(f'path: "{args["src"]}" does not exist')
    if args["add"] and not os.path.isdir(args["add"]):
        raise SystemExit(f'path: "{args["src"]}" is not a directory')
    return args

def main() -> None:
    """Main cli function, parses arguments and exeuctes commands against image search engine.
    """    
    engine = Engine()
    args = parseArgs()
    
    if args["add"]:
        engine.add(args["add"])
    elif args["search"]:
        pass
    elif args["info"]:
        engine.info()

if __name__ == "__main__":
    main()