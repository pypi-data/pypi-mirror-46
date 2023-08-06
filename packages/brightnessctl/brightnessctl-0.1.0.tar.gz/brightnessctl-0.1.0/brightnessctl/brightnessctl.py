#!/bin/env python3
from time import sleep
import argparse
from pathlib import Path
from functools import lru_cache


class Brightness(object):
    path = Path("/sys/class/backlight/intel_backlight")

    @property
    def current(self) -> int:
        with open(self.path / "actual_brightness") as f:
            return int(f.read().strip())

    @property
    def current_percent(self) -> float:
        return self.current / self.max * 100

    @property
    @lru_cache(maxsize=512)
    def max(self) -> int:
        with open(self.path / "max_brightness") as f:
            return int(f.read().strip())

    def set(self, value: int):
        value = min(value, self.max)
        value = max(value, 0)
        with open(self.path / "brightness", 'w') as f:
            f.write(f"{int(value)}")

    def save(self):
        with open("/tmp/backlight", "w") as f:
            f.write(f"{self.current_percent}")

    def load(self) -> float:
        with open("/tmp/backlight", "r") as f:
            return float(f.read().strip())

    def smooth_step(self, percent: float, duration: float):
        """ Smoothly scale to the desired percent. """
        starting_brightness = self.current
        steps = int(duration * 150)  # 150 steps per second
        sleep_duration = duration / steps

        desired_value = self.max * (percent / 100)

        delta = (desired_value - starting_brightness) / steps

        for step in range(1, steps+1):
            step_value = starting_brightness + delta * step
            self.set(step_value)
            if step != steps:
                sleep(sleep_duration)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    change_group = parser.add_mutually_exclusive_group()
    change_group.add_argument(
        "-p",
        "--percent",
        metavar="N",
        type=float,
        help="Set brightness to <N> %%")
    change_group.add_argument(
        "-d",
        "--delta",
        metavar="N",
        type=float,
        default=0,
        help="Adjust brightness by <N> %% of max brightness")
    change_group.add_argument(
        "-r",
        "--relative",
        metavar="N",
        type=float,
        default=0,
        help="Adjust brightness by <N> %% of current brightness")

    parser.add_argument(
        "--duration",
        metavar="S",
        type=float,
        default=0.1,
        help="How long to take to get to final value")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--save",
        action="store_true",
        default=False,
        help="Save current value to disk before changing value")
    group.add_argument(
        "--restore",
        action="store_true",
        default=False,
        help="Restore saved value from disk")
    args = parser.parse_args()

    bc = Brightness()
    percent = args.percent
    current_percent = bc.current_percent

    if args.delta:
        percent = current_percent + args.delta
    elif args.relative:
        percent = current_percent * (args.relative / 100)

    if args.verbose:
        print(f"Scaling from {current_percent} to {percent}")

    if args.restore:
        percent = bc.load()

    if args.save:
        bc.save()

    bc.smooth_step(percent, args.duration)


if __name__ == "__main__":
    main()
