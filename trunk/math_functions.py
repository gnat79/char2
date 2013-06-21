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

from math import log, ceil

# Make a 2x2 array of values, a multiplication table.
def getTable(q,p):
    n = pow(2,q) - 1
    table = []
    table.append([0]*(n+1))
    for i in range(1,n + 1):
        row = [0]
        for j in range(1,n + 1):
            row.append(multiply(i,j,p,q))
        table.append(row)
    return table

# Prints the multiplication table.
def printTable(table):
    size = len(table[1])
    wordLength = 0
    for i in range(size):
        word = printElt(i+1)
        if len(word) > wordLength:
            wordLength = len(word)
    overline = '+' + '-'*(wordLength+2)

    print '-' *((size - 1) * (wordLength + 3) + 1)
    for row in table[1:]:
        rowString = '| '
        for code in row[1:]:
            elt = printElt(code)
            sizeOfElement = len(elt)
            if sizeOfElement < wordLength:
                elt += ' '*(wordLength - sizeOfElement)
            rowString += elt + ' | '
        print rowString
        print overline * (size - 1) + '+'

# Multiply a and b, given the irreducible polynomial p and the size of the 
# field q = 2^r. Here a and b are elements of F_q and the field has 
# n = 2^q - 1 non-zero elements.
def multiply(a, b, p, q):
    result = []
    v = bv(a)
    w = bv(b)
    long = []
    short = []
    n = pow(2,q)

    #find the short array
    if len(v) >= len(w):
        long = v
        short = w
    else:
        long = w
        short = v
    size = len(long)

    #pad the shorter array
    short.reverse()
    for x in range(len(short), size):
        short.append(0)
    short.reverse()
    
    #multiply short * long
    tempv = []
    addends = []
    for x in range(size):
        temp = scale(short[size-x-1], long)
        for y in range(x):
            temp.append(0)
        addends.append(temp)
    for x in range(len(addends)):
        result = xor(result, addends[x])
    #if the number is bigger than the polynomial, mod xor that with p.
    intval = bv2int(result)
    while intval >= n:
        result = reduce(result, p)
        intval = bv2int(result)
        result = bv(intval)
        
    return intval

# Reduce an element to standard form.
# Eg, a^3 + a + 1 is not in F_4, so reduce it using a^2 + a + 1 = 0.
def reduce(vector, p):
    vec = vector[:]
    poly = bv(p)
    l = len(vector)
    diff = l - len(poly)
    temp = poly[:]
    for x in range(diff):
        temp.append(0)
    vec = xor(vec, temp)
    return vec

# Scale a vector by 1 or 0.
def scale(scalar, vector):
    result = []
    for x in range(len(vector)):
        result.append(scalar*vector[x])
    return result

# XOR the bits of two arrays.
def xor(a, b):
    result = []
    long = []
    short = []

    #find the short array
    if len(a) >= len(b):
        long = a
        short = b
    else:
        long = b
        short = a

    #pad the shorter array
    short.reverse()
    for x in range(len(short), len(long)):
        short.append(0)
    short.reverse()

    #do the xor operation
    for i in range(len(short)):
        result.append(long[i]^short[i]);
    for i in range(len(short), len(long)):
        result.append(long[i])

    return result

# Compute the binary representation of an integer, a vector of binary digits.
def bv(a):
    b = a
    result = []
    for i in range(1,len(bin(a))-1):
        result.append(b%2)
        b = b/2
    result.reverse()
    return result

# Converts a vector of binary digits to an integer.
def bv2int(v):
    v.reverse()
    result = 0
    for s in range(len(v)):
        result = result + v[s]*pow(2,s)
    v.reverse()
    return result

# Add two field elements.
def addElts(a,b):
    u = bv(a)
    v = bv(b)
    w = xor(u,v)
    return bv2int(w)

# Convert an element to a string.
def printElt(elt):
    if elt < 1:
        return '0'
    char = bv(elt)
    n = len(char)
    result = ''
    list = [i for i in reversed(range(len(char)))]
    for i in range(len(char)):
        if i == 0:
            if len(char) > 2:
                result = 'a^%i' % (list[i])
            if len(char) == 2:
                result = 'a'
            if len(char) == 1:
                result = '1'
            if len(char) == 0:
                result = '0'
        elif (i < n-2 and char[i] == 1):
            result = result + ' + a^%i' % (n-i-1)
        elif (i == n-2 and char[i] == 1):
            result = result + ' + a'
        elif (i == n-1 and char[i] == 1):
            result = result + ' + 1'
    return result
