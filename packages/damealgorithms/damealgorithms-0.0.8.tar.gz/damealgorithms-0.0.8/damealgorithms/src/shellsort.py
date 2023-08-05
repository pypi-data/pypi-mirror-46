#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2018  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,


class Graph(object):
    def __init__(self, alist):
        self.alist = alist

    def shellSort(self):
        sublistcount = len(self.alist)//2
        while sublistcount > 0:

            for startposition in range(sublistcount):
                self.gapInsertionSort(startposition,sublistcount)

                print("After increments of size",sublistcount,
                                   "The list is",self.alist)

            sublistcount = sublistcount // 2

    def gapInsertionSort(self,start,gap):
        for i in range(start+gap,len(self.alist),gap):

            currentvalue = self.alist[i]
            position = i

            while position>=gap and self.alist[position-gap]>currentvalue:
                self.alist[position]=self.alist[position-gap]
                position = position-gap

            self.alist[position]=currentvalue

g = Graph([54,26,93,17,77,31,44,55,20])
g.shellSort()
print(g.alist)
# alist = [54,26,93,17,77,31,44,55,20]
# shellSort(alist)
# print(alist)
