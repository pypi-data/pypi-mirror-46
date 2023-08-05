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
from src.hamiltonian import Graph

class TestHamiltonian(TestCase):

    def test_hamiltonian_create(self):
        ''' Let us create the following graph
        (0)--(1)--(2)
        |   / \   |
        |  /   \  |
        | /     \ |
        (3)-------(4)    '''
        g1 = Graph(5)
        g1.graph = [ [0, 1, 0, 1, 0], [1, 0, 1, 1, 1],
                     [0, 1, 0, 0, 1,],[1, 1, 0, 0, 1],
                     [0, 1, 1, 1, 0], ]

        self.assertEqual([0, 1, 2, 4, 3,], g1.hamCycle())
        ''' Let us create the following graph
        (0)--(1)--(2)
        |   / \   |
        |  /   \  |
        | /     \ |
        (3)       (4)    '''
        g2 = Graph(5)
        g2.graph = [ [0, 1, 0, 1, 0], [1, 0, 1, 1, 1],
                     [0, 1, 0, 0, 1,], [1, 1, 0, 0, 0],
                     [0, 1, 1, 0, 0], ]

        self.assertEqual(False, g2.hamCycle())
