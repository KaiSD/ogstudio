#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Shuan gameplay prototype cProfile data viewer
(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

import pstats
p = pstats.Stats('gameinfo.profile')

p.strip_dirs().sort_stats('cumulative').print_stats()