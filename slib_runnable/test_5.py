#    Copyright 2022 Ian Paul
#    Copyright 2009 Thomas Gideon
#
#    This file is part of flashbake.
#
#    flashbake is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    flashbake is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with flashbake.  If not, see <http://www.gnu.org/licenses/>.

import subprocess


def addignored(ignored):
    ''' Use the git command to obtain the file names, turn it into a list, sort the list for only ignored files, return those files as a single string with each filename separated by a comma.'''
    fldr=subprocess.run(["git", "-C", ignored, "status", "-s", "--ignored"], capture_output=True, text=True).stdout.strip("\n")
    x = fldr.splitlines()
    sub = "!"
    g = ([s for s in x if sub in s])
    i = [elem.replace(sub, '') for elem in g]
    t = ", ".join(i)
    return t




def test_addignored():
    """Check the correctness of addignored
    """
    assert addignored(".") == " ../self_contained/.pytest_cache/,  .pytest_cache/"

