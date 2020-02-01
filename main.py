from game import *
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-f", "--fullscreen", help="makes game fullscreen", action="store_true")
    parser.add_argument("--width", help="game window width", type=int)
    parser.add_argument("--height", help="game window height", type=int)
    args = parser.parse_args()

    game_instance = Game(GameOptions(
        verbose=args.verbose,
        fullscreen=args.fullscreen,
        width=args.width,
        height=args.height
    ))

    game_instance.start()


if __name__ == "__main__":
    main()
