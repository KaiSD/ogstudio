#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Simplui for Cocos2d

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

from cocos.director import director
from cocos import batch
from simplui import *

class CocosUIFrame(batch.BatchNode):
    def __init__(self, theme='data/ui', interactive=True):
        super(batch.BatchNode, self).__init__()
        width, height = director.get_window_size()
        self.ui = Frame(Theme(theme), w=width, h=height)
        self.batch = self.ui.batch
        self.interactive = interactive
    
    def add(self, item):
        self.ui.add(item)
    
    def remove(self, item):
        self.ui.remove(item)
    
    def draw(self):
        pass
    
    def visit(self):
        self.ui.draw()
    
    def on_enter(self):
        super(batch.BatchNode, self).on_enter()
        if self.interactive:
            director.window.push_handlers(self)
    
    def on_exit(self):
        super(batch.BatchNode, self).on_exit()
        if self.interactive:
            director.window.remove_handlers(self)
    
    def on_mouse_press(self, x, y, btn, mod):
        nx, ny, = director.get_virtual_coordinates(x, y)
        self.ui.on_mouse_press(int(nx), int(ny), btn, mod)
    
    def on_mouse_release(self, x, y, btn, mod):
        nx, ny, = director.get_virtual_coordinates(x, y)
        self.ui.on_mouse_release(int(nx), int(ny), btn, mod)
    
    def get_element_by_name(self, name):
        return self.ui.get_element_by_name(name)