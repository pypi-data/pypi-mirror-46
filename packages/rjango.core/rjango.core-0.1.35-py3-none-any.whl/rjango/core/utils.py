import typing
import logging
from termcolor import colored


def print_block(
    messages: typing.List[typing.AnyStr], color_msg="green", color_block=None
):
    block = "########################"
    if color_block is None:
        color_block = color_msg

    print(colored(block, color_block))
    for m in messages:
        print(colored(m, color_msg))

    print(colored(block, color_block))
