#!/usr/bin/env python3
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>
#

import subprocess
import os

def main():
    # Initialize variables
    output = ""
    previous_line = ""
    folder = ""
    prefix = ""
    otp=""
    leave_folder = False

    # By clicking an entry, the user calls
    # 'pass <entry> | wl-copy' when on wayland or
    # 'pass <entry> | xclip' when on X11
    command = "|bash='pass "
    suffix  = "|wl-copy -n' terminal=false"
    if os.environ["XDG_SESSION_TYPE"]!="wayland":
        suffix = "|xclip terminal=false"

    # Let's go:
    ## The icon for the gnome bar
    print("|iconName=dialog-password")
    print("---")

    ## Call pass for the output
    try:
        output = subprocess.check_output(["pass", "ls"])
        output = output.decode('UTF-8').splitlines()
    except:
        print("Error calling pass. Is it installed?")

    ## Remove the first line saying "Password Store"
    output = output[1:]

    ## Now comes the tricky part. We have two jobs:
    ## 1. Print the output so that Argos can render a dropdown menu
    ## 2. Append the command "pass <entry> | wl-copy -n" to each entry
    ##
    ## To do those jobs, we need to find out whether a line in output is
    ## a folder or an actual entry. We can't find that out by looking at each
    ## on its own. That's why on the first run of the for loop, we write
    ## `line` to `previous_line`. Then, beginning from the second run, we
    ## actually do our stuff. For the last line, we have to do it after then
    ## for-loop.
    for line in output:
        ## get rid of the first 5 characters
        line = line[4:]

        if line.startswith("├") or line.startswith("└"):
            prefix = "--"
            line = line[4:]
            if not folder:
                folder = previous_line
        else:
            if folder:
              # we were in a folder, but have left it
              leave_folder = True

        if previous_line:
            if folder==previous_line:
                print(folder)
                if "otp" in folder:
                    otp="otp "
            elif folder:
                print(prefix+previous_line+command+otp+folder+"/"+previous_line+suffix)
            else:
                print(prefix+previous_line+command+previous_line+suffix)

        previous_line = line
        if leave_folder:
            folder = ""
            prefix = ""
            otp = ""
            leave_folder = False

    # write the last line
    print(prefix+previous_line+command+otp+folder+"/"+previous_line+suffix)

    print("---")
    print("refresh | refresh=true")

main()
