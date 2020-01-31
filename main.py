import game
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    game.start(args.verbose)


if __name__ == "__main__":
    main()
