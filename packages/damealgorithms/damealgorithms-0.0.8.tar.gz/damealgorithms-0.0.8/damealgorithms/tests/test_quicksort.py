#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

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

from unittest import TestCase
from src.quicksort import Quicksort

class TestBasics(TestCase):

    def test_quicksort_create(self):
        alist = [54,26,93,17,77,31,44,55,20]
        q = Quicksort(alist)
        self.assertEqual([54,26,93,17,77,31,44,55,20], q.vector)

    def test_quicksort_helper(self):
        alist = [54,26,93,17,77,31,44,55,20]
        q = Quicksort(alist)
        self.assertEqual(None, q.quickSortHelper(alist, 54, 20))
        
    # def test_quicksort_partition(self):
    #     l = [54,26,93,17,77,31,44,55,20]
    #     q = Quicksort(l)
    #     self.assertEqual([54, 26], q.partition(l, 0, 1))


    # def test_quicksort_quicksort(self):
    #     alist = [54,26,93,17,77,31,44,55,20]
    #     q = Quicksort(alist)
    #     self.assertEqual([54,26,93,17,77,31,44,55,20], q.quickSort(alist))
