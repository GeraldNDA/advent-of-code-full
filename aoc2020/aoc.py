#!/usr/bin/env python3
from genericpath import exists
import stat

from datetime import datetime
from requests import Session
from pathlib import Path
from argparse import ArgumentParser
from runpy import run_path

class AdventOfCode():
    AOC_SESSION_FILE = ".aocinfo"
    AOC_SESSION_PATHS = (
        Path.cwd(),
        Path.home()
    )
    AOC_DEFAULT_SCRIPT = "default_script.aoc"
    AOC_YEARS = range(2018, datetime.now().year if datetime.now().month < 12 else datetime.now().year + 1)
    AOC_DAYS = range(1, 26)

    def __init__(self, *, year, day):
        assert day in AdventOfCode.AOC_DAYS
        assert year in AdventOfCode.AOC_YEARS
        self.day = day
        self.year = year

        for path in AdventOfCode.AOC_SESSION_PATHS:
            path = path / AdventOfCode.AOC_SESSION_FILE
            if path.exists():
                with path.open() as aoc_session:
                    self.session = Session()
                    self.session.cookies['session'] = aoc_session.read().strip()
                break
        else:
            raise ValueError(f"Could not find '{AdventOfCode.AOC_SESSION_FILE}'.")

    def get_input(self, raw=False):
        input_files = Path(f"day{self.day}.txt"), Path(f"day{self.day}/day{self.day}.txt")
        chosen_file = None
        for input_file in input_files:
            if input_file.exists():
                chosen_file = input_file
                grabbed_time = datetime.fromtimestamp(chosen_file.stat().st_mtime)
                input_release = datetime(self.year, 12, self.day)
                if input_release > grabbed_time:
                    continue

        puzzle_input = []

        if not chosen_file:
            print("Updating...")
            with self.session as session:
                response = session.get(f"https://adventofcode.com/{self.year}/day/{self.day}/input", stream=True)
                response.raise_for_status()
                with open(input_files[-1], "bw") as contents:
                    for line  in response.iter_lines():
                        if line:
                            if not raw:
                                puzzle_input.append(line.decode('utf-8').strip())
                            else:
                                puzzle_input.append(line.decode('utf-8'))
                        contents.write(line)
                        contents.write(b"\n")
        else:
            with open(chosen_file) as contents:
                if not raw:
                    puzzle_input = list(map(lambda l: l.strip(), contents.readlines()))
                else:
                    puzzle_input = list(map(lambda l: l.strip("\n"), contents.readlines()))

        if not puzzle_input:
            return None
        elif len(puzzle_input) == 1:
            return puzzle_input[0]
        return puzzle_input

    @staticmethod
    def _get_default_aoc(day=None, year=None):
        if day:
            assert day in AdventOfCode.AOC_DAYS, f"Got out of range day {day}"
        if year:
            assert year in AdventOfCode.AOC_YEARS, f"Got out of range year {year}"

        now  = datetime.now()
        if now.month == 12:
            if now.day <= 25:
                # if it's december, then default to today
                now = now
            else:
                # if it's december after christmas, default to Dec. 1st
                now = datetime(year=now.year, month=now.month, day=1)
        else:
            # if it's not december, default to last year's puzzle
            now = datetime(year=now.year-1, month=12, day=1)

        # Either use provided value or default value (single day can be provided, default year is used)
        return datetime(year=year or now.year, month=now.month, day=day or now.day)

    @staticmethod
    def generate(day=None, year=None):
        now = AdventOfCode._get_default_aoc(day, year)
        
        script_content = None
        with Path(AdventOfCode.AOC_DEFAULT_SCRIPT).open() as script_template:
            script_content = script_template.read().format(day=now.day, year=now.year)
        if not script_content:
            raise ValueError("Encountered an issue loading the template")

        script_dir = Path(f"day{now.day}")
        script_names = (
            f"day{now.day}_1.py",
            f"day{now.day}_2.py",
        )
        print(f"Generating scripts ...")
        script_dir.mkdir(exist_ok=True)
        # set up file structure
        for script_name in script_names:
            script_path = script_dir / script_name
            if not script_path.exists():
                with script_path.open("w") as script:
                    script.write(script_content)
                script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)
            print(f"\t Generated {str(script_path)}")
        print(f"Generated all scripts")

    @staticmethod
    def run(day=None, year=None, part=1):
        now = AdventOfCode._get_default_aoc(day, year)
        script_path = Path(f"day{now.day}/day{now.day}_{part}.py")
        print(f"Running {str(script_path)} ...")
        run_path(script_path)

def parse_args():
    parser = ArgumentParser(description="Wrapper for quickly creating and running aoc scripts")
    parser.set_defaults(runner=AdventOfCode.generate)
    subparsers = parser.add_subparsers()

    run_command = subparsers.add_parser("run", help="Run a generated AOC script")
    run_command.add_argument("day",  nargs='?', type=int, metavar="DAY", choices=AdventOfCode.AOC_DAYS, help="AOC Puzzle Day")
    run_command.add_argument("part",  nargs='?', type=int, metavar="PART", default=1, choices=(1, 2), help="AOC Puzzle Part")
    run_command.add_argument("year",  nargs='?', type=int, metavar="YEAR", choices=AdventOfCode.AOC_YEARS, help="AOC Year")
    run_command.set_defaults(runner=AdventOfCode.run)
    
    generate_command = subparsers.add_parser("gen", help="Run a generated AOC script")
    generate_command.add_argument("day",  nargs='?', type=int, metavar="DAY", choices=AdventOfCode.AOC_DAYS, help="AOC Puzzle Day")
    generate_command.add_argument("year",  nargs='?', type=int, metavar="YEAR", choices=AdventOfCode.AOC_YEARS, help="AOC Year")
    generate_command.set_defaults(runner=AdventOfCode.generate)

    args = vars(parser.parse_args())
    runner = args.pop("runner")
    runner(**args)
    # print(runner, args)


if __name__ == "__main__":
    parse_args()