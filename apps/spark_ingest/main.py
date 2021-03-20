"""
"""
import asyncio
from datetime import datetime
import logging

import boto3
import click
from sqlalchemy import create_engine

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s]: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)

logger = logging.getLogger(__name__)


def edit_distance(s1: str, s2: str) -> int:
    memo = [[0]*(len(s2) + 1) for _ in range(len(s1) + 1)]

    for i1 in range(1, len(s1) + 1):
        for i2 in range(1, len(s2) + 1):
            if i1 == 0:
                memo[i1][i2] = i2
            elif i2 == 0:
                memo[i1][i2] = i1
            elif s1[i1 - 1] == s2[i2 - 1]:
                memo[i1][i2] = memo[i1 - 1][i2 - 1]  # same
            else:
                memo[i1][i2] = 1 + min(memo[i1 - 1][i2 - 1],  # same
                                       memo[i1 - 1][i2],  # delete s1
                                       memo[i1][i2 - 1]  # insert s1
                                       )

    return memo[-1][-1]


def test_algo(n) -> int:
    total, ones, zeros = 2, 1, 1
    for bin_len in range(2, n + 1):
        tmp_ones = zeros
        zeros = ones + zeros
        ones = tmp_ones
        total = ones + zeros

    return total


@click.command()
@click.option('--asynchronous/--no-asynchronous', default=True,
              show_default=True, help='Set/unset asynchronous behavior')
def main(asynchronous: bool) -> None:
    """
    """
    print(test_algo(4))
    print(test_algo(5))


if __name__ == "__main__":

    main()
