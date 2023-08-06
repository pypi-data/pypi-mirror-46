# Copyright (C) 2019 Michał Góral.
#
# This file is part of TWC
#
# TWC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TWC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TWC. If not, see <http://www.gnu.org/licenses/>.

'''Utility functions'''

import sys

from prompt_toolkit.application.current import get_app
from prompt_toolkit.formatted_text import to_formatted_text


def pprint(text):
    '''Print some text in prompt_toolkit-friendly way.'''
    if not text:
        return

    try:
        controller = get_app().controller()
    except AttributeError:  # no controller or controller() is None
        print(text)
        return

    ft = to_formatted_text(text)
    controller.commandline.print(ft)


def eprint(text):
    '''Print error in prompt_toolkit-friendly way.'''
    if not text:
        return

    try:
        controller = get_app().controller()
    except AttributeError:  # no controller or controller() is None
        print(text, file=sys.stderr)
        return

    ft = to_formatted_text(text, style='class:error')
    controller.commandline.print(ft)
