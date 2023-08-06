import argparse

from hankey.main import run, restore

parser = argparse.ArgumentParser(prog="hankey", description='Hankey Dumper')
subparsers = parser.add_subparsers(help='sub-command help', dest="command")
subparsers.required = True

parser_run = subparsers.add_parser('run', help='run help')

parser_restore = subparsers.add_parser('restore', help='restore help')
parser_restore.add_argument('job', type=str, help='job name')

args = parser.parse_args()

if args.command == 'run':
    try:
        run()
    except Exception as e:
        print(e)
    print("Finished")

elif args.command == "restore":
    job = args.job
    try:
        restore(job)
    except Exception as e:
        print(e)
    print("Finished")


def main():
    print("Greetings from Mr. Hankey")
