import argparse
from kid import make, verify


def argparser():
    parser = argparse.ArgumentParser(description='Generate or verify KID in either MOD10 or MOD11')
    parser.add_argument('-m', '--mode', choices=['MOD10', 'MOD11'], type=str.upper, default='MOD10', help='Choose MOD10 or MOD11 (defaults to MOD10)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', '--generate', metavar='KID', type=str, help='Generate KID from integer string')
    group.add_argument('-v', '--verify', metavar='KID', type=str, help='Verify validity of KID string')

    return parser.parse_args()


if __name__ == "__main__":
    args = argparser()

    if args.generate:
        print(make(args.generate, args.mode))
    elif args.verify:
        print(verify(args.verify, args.mode))
