# This file is part of char2.

# char2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# char2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with char2.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2013 Nathaniel Schwartz.

from math_functions import *
from math import pow, log
import sys

mtable = []         # Mulitplication table
r = -1              # The power of the field. The field will have size 2^r
poly = -1           # The irreducible (over {1,0}) polynomial for the field
setup = False       # Set to True when the field size and polynomial are set
register = -1       # The register for the calculator. Currently not functional


# Process command line options.
def getOption():
    option = raw_input("2=0: ").upper()
    cmd = option[0]
    if (cmd == 'Q'): 
        exit()
    elif (cmd == 'S'):
        size(option[1:])
    elif (cmd == 'P'): 
        polynomial(option[1:])
    elif (cmd == 'T'): 
        table(option[1:])
    elif (cmd == 'R'):
        reset()
    elif (cmd == 'V'):
        view()
    elif option.find('+')>= 0:
        add(option)
    elif option.find('*') >= 0:
        multiply(option)
    else:
        print "Invalid option."

# Print the list of options so the user has information to make a choice.
def printOptions():
    print '='*73
    print 'Welcome to char2, a calculator for fininte fields in even characteristic.'
    print '='*73
    print "R\tReset the state of the program"
    print "S\tSet the size of the field"
    print "P\tSet the polynomial - takes an integer (eg. 7 -> 111 -> a^2 + a + 1)"
    print "T\tPrints the multiplication table - (1 -> numbers, 0 -> strings)"
    print "V\tView the current setup"
    print "Q\tQuits the program"
    print '\n'

# Convert the command line string (of an integer) to an integer.
def polynomial(string):
    input = ''
    try:
        input = int(string.split()[0])
    except IndexError:
        print "Try again."
        return
    if input > 2:
        global poly
        poly = input
    else:
        raise ValueError("Invalid polynomial.")
    # Here we go ahead and create the multiplication table if we can.
    if r > 0:
        global mtable
        global setup
        mtable = getTable(r,poly)
        setup = True
    
# Multiply some elements of the field.
def multiply(multiplicands):
    global register
    x = -1
    loc = multiplicands.split('*')
    if setup:
        try:
            x = int(loc[0])
        except ValueError:
            x = -1
        if (x < 0 and register > 0):
            x = register
        else: 
            print "Register is empty!"
            return
        try: 
            y = int(loc[1])
        except ValueError:
            print "Invalid multiplication input."
            return
        global mtable
        try:
            elt = mtable[x][y]
        except IndexError:
            print "Element isn't in the defined field."
            return
        print printElt(elt) + "\t[" +  str(elt) + "]"
        register = elt
    else:
        print "Set options first!"

# Add some elements of the field.
def add(summands):
    x = -1
    global register
    loc = summands.split('+')
    if setup:
        try:
            x = int(loc[0])
        except ValueError:
            x = -1
        if (x < 0 and register > 0):
            x = register
        else:
            print "Register is empty!"
            return
        try:
            y = int(loc[1])
        except ValueError:
            print "Invalid addition input."
            return
        elt = addElts(x,y)
        print str(printElt(elt)) + "\t[" + str(elt) + "]"
        register = elt
    else:
        print "Set options first!"

# Print the multiplication table, either in integer or string format.
def table(option):
    input = ''
    try:
        input = int(option.split()[0])
    except IndexError:
        print "Try again."
        return
    if input == 0:
        printTable(mtable)
    elif input == 1:
        for row in mtable[1:]:
            print row[1:]
    else:
        raise ValueError("Invalid Table Option.")

# Set the size of the field. User input should be the size. We convert it to 
# the power of 2 here.
def size(option):
    try:
        value = int(option.split()[0])
    except IndexError:
        print "Invalid size argument."
        return
    if value > 1:
        global r
        rtmp = int(log(value,2))
        if pow(2, rtmp) != value:
            print 'Field size should be a power of 2.'
            return
        else:
            r = rtmp
    else:
        raise ValueError("Invalid integer.")
    if poly > 0:
        global mtable
        global setup
        mtable = getTable(r,poly)
        setup = True

# View the current field setup.
def view():
    if r > 1:
        print 'The field has', int(pow(2,r)), 'elements, and the polynomial is', printElt(poly),
    else:
        print 'The field is not defined yet.'

# Reset the field setup.
def reset():
    global mtable
    global r
    global poly
    global setup
    mtable = []
    r = -1
    poly = -1
    setup = False
    register = -1

# EXECUTION LOOP
# ==============
# This is the main loop which runs the program
printOptions()
while(True):
    try:
        getOption()
    except ValueError as e:
        print e
