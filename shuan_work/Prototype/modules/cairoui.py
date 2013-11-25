#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Cairo ui for Cocos2d

WARNING. THIS MODULE IS INCOMPLETE. DO NOT USE IT!

(c) 2012 Opensource Game Studio Team (http://opengamestudio.org)
'''

import ctypes
import cairo
from cocos import sprite
from pyglet import image
import Image

class UiElement:
    def __init__(self, *args, **kwargs):
        
        self.geometry = []
        for i in args:
            if type(i) in (tuple, list):
                self.geometry.append(tuple(i))
        
        self.visible = True
        self.active = True
        
        self.id = kwargs.get('id', '')
        
        self.handlers = {
                         'mouseEnter': kwargs.get('mouseEnter', None),
                         'mouseLeave': kwargs.get('mouseLeave', None),
                         'mousePress': kwargs.get('mousePress', None),
                         'mouseRelease': kwargs.get('mouseRelease', None),
                         }
        
        self._context = None
        self._parent = None
    
    def addGeometry(self, geo):
        if type(geo) in (tuple, list):
            self.geometry.append(tuple(geo))
        
    def drawContext(self):
        if not self.visible:
            return
        
        context = self._context
        
        cairoCommands = {
                      'rect': context.rectangle,
                      'set_rgba': context.set_source_rgba,
                      'fill': context.fill,
                      }
        
        for cmd in self.geometry:
            cairoCommands[cmd[0]](*cmd[1:])
    
    def pointerCheck(self, x, y):
        cr = self._context
        if cr:
            return cr.in_fill(x, y)

class CairoUI(sprite.Sprite):
    def __init__(self, w, h, *elements, **kwargs):
        self._elements = []
        self._namedElements = {}
        
        data = (ctypes.c_ubyte * w * h * 4)()
        
        pitch = w * 4
        surface = cairo.ImageSurface.create_for_data (data, cairo.FORMAT_ARGB32, w, h, pitch);
        context = cairo.Context(surface)
        self.surface = surface
        self.context = context
        self.size = w, h
        self.pitch = pitch

        for e in elements:
            if issubclass(e.__class__, UiElement):
                self.add(e)
                e.drawContext()
        
        imgdata = Image.frombuffer('RGBA', (w, h), surface.get_data(),
                                   'raw', 'BGRA', 0, 1).tostring('raw', 'RGBA', 0, 1)
        
        img = image.create(w, h)
        img.set_data('RGBA', pitch, imgdata)
        
        super(CairoUI, self).__init__(img)
        
        self.needRedraw = False
        self.hasPointer = False
        self.interactive = kwargs.get('interactive', True)
        
        self.schedule(self.drawElements)
    
    def add(self, element):
        element._context = cairo.Context(self.surface)
        element._parent = self 
        if element.id:
            self._namedElements[id] = element
        self._elements.append(element)
        self.needRedraw = True
    
    def getElement(self, id):
        return self._namedElements[id]
    
    def drawElements(self, dt):
        surface = self.surface
        context = self.context
        
        context.set_source_rgba(0, 0, 0, 0)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        
        w, h = self.size
        pitch = self.pitch
        
        for i in self._elements:
            i.drawContext()
        
        imgdata = Image.frombuffer('RGBA', (w , h),
        surface.get_data(), 'raw', 'BGRA', 0, 1).tostring('raw', 'RGBA', 0, 1)
        
        img = image.create(w, h)
        img.set_data('RGBA', pitch, imgdata)
        
        self.image = img
    
    def on_mouse_press(self, x, y, btn, mod):
        print "press"
        if not self.interactive:
            return
        aabb = self.get_AABB()
        if aabb.contains(x, y):
            rx, ry = int((x - aabb.left)/self.scale), int((y - aabb.bottom)/self.scale)
            for i in self._elements:
                if i.pointerCheck(x, y):
                    i.hasPointer = True
                    func = i.handlers.get('MousePress', None)
                    if func:
                        func(btn, mod)
    
    def on_mouse_release(self, x, y, btn, mod):
        print "release"
        if not self.interactive:
            return
        aabb = self.get_AABB()
        if aabb.contains(x, y):
            rx, ry = int((x - aabb.left)/self.scale), int((y - aabb.bottom)/self.scale)
            for i in self._elements:
                if i.pointerCheck(x, y):
                    func = i.handlers.get('MouseRelease', None)
                    if func:
                        func(btn, mod)
    
    def on_mouse_motion(self, x, y, dx, dy):
        print "motion"
        if not self.interactive:
            return
        aabb = self.get_AABB()
        if aabb.contains(x, y):
            rx, ry = int((x - aabb.left)/self.scale), int((y - aabb.bottom)/self.scale)
            for i in self._elements:
                if i.pointerCheck(x, y):
                    i.hasPointer = True
                    func = i.handlers.get('MouseEnter', None)
                    if func:
                        func()
                elif i.hasPointer:
                    func = i.handlers.get('MouseLeave', None)
                    if func:
                        func()