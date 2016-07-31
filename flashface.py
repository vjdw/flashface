#!/usr/bin/env python

import unicornhat as unicorn
import time
import numpy as np
import web
import threading

class UnicornDisplay:
  unicorn.set_layout(unicorn.AUTO)
  unicorn.rotation(180)
  unicorn.brightness(0.3)
  screenWidth,screenHeight=unicorn.get_shape()

  glyphHeight = 4
  glyphSpacing = 1
  scrollXOffset = -screenWidth
  message = ""
  messagePixels = np.zeros((1, glyphHeight), dtype=np.bool)

  def start(self):
    t = threading.Thread(target=self.runDisplay)
    t.daemon = True
    t.start()

  def runDisplay(self):
    print('Display loop started.')
    global scrollXOffset
    scrollXOffset = -self.screenWidth
    while True:
      unicorn.clear()
      for screenx in range(self.screenWidth):
        for screeny in range(self.screenHeight):
          screenxOffset = screenx + scrollXOffset
          if (screenxOffset >= 0) and (screenxOffset < len(self.messagePixels)) and (self.messagePixels[screenxOffset][screeny]):
            unicorn.set_pixel(screenx, screeny, 50,100,150)  
      unicorn.show()
      scrollXOffset += 1
      if scrollXOffset > len(self.messagePixels):
        scrollXOffset = -self.screenWidth 
      time.sleep(0.05)

  def setMessage(self, message):
    print('Display message received: ' + message)
    global scrollXOffset
    messageGlyphs = []
    for ch in message:
      if ch in self.glyphMap:
        messageGlyphs.append(self.glyphMap[ch])
      else:
        messageGlyphs.append(self.glyphMap['unknown'])

    # Calculate and set the width of the messagePixels array.
    messageWidth = 0
    for glyph in messageGlyphs:
      messageWidth += len(glyph[0])
      if glyph is not self.space:
        messageWidth += self.glyphSpacing
    messageWidth = max(messageWidth, self.screenWidth)
    self.messagePixels = np.zeros((messageWidth, self.glyphHeight), dtype=np.bool)

    # Copy each glyph bitmap to messagePixels array.
    glyphOffset = 0
    for glyph in messageGlyphs:
      for x in range(len(glyph[0])):
        for y in range(self.glyphHeight):
          self.messagePixels[x+glyphOffset][y] = glyph[y][x]
      glyphOffset += len(glyph[0])
      if glyph is not self.space:
        glyphOffset += self.glyphSpacing

    scrollXOffset = -self.screenWidth 

  a = [[0,1,0],[1,0,1],[1,1,1],[1,0,1]]
  b = [[1,0,0],[1,1,0],[1,0,1],[1,1,0]]
  c = [[0,1,1],[1,0,0],[1,0,0],[0,1,1]]
  d = [[1,1,0],[1,0,1],[1,0,1],[1,1,0]]
  e = [[0,1,1],[1,0,1],[1,1,0],[0,1,1]]
  f = [[0,1,1],[1,0,0],[1,1,0],[1,0,0]]
  g = [[0,1,1],[1,0,0],[1,0,1],[0,1,1]]
  h = [[1,0,0],[1,1,0],[1,0,1],[1,0,1]]
  i = [[1,1,1],[0,1,0],[0,1,0],[1,1,1]]
  j = [[0,0,1],[0,0,1],[1,0,1],[0,1,0]]
  k = [[1,0,1],[1,1,0],[1,1,0,0],[1,0,1]]
  l = [[1,0],[1,0],[1,0],[1,1]]
  m = [[0,1,1,0],[1,1,1,1],[1,1,1,1],[1,0,0,1]]
  n = [[1,0,0,1],[1,1,0,1],[1,0,1,1],[1,0,0,1]]
  o = [[0,1,0],[1,0,1],[1,0,1],[0,1,0]]
  p = [[1,1,0],[1,0,1],[1,1,0],[1,0,0]]
  q = [[0,1,1,0],[1,0,1,0],[0,1,1,0],[0,0,1,1]]
  r = [[0,1,1],[1,0,0],[1,0,0],[1,0,0]]
  s = [[0,1,1],[1,1,0],[0,1,1],[1,1,0]]
  t = [[1,1,1],[0,1,0],[0,1,0],[0,1,0]]
  u = [[1,0,1],[1,0,1],[1,0,1],[1,1,1]]
  v = [[1,0,1],[1,0,1],[1,0,1],[0,1,0]]
  w = [[1,0,0,1],[1,1,1,1],[1,1,1,1],[0,1,1,0]]
  x = [[1,0,1],[0,1,0],[0,1,0],[1,0,1]]
  y = [[1,0,1],[1,0,1],[0,1,0],[0,1,0]]
  z = [[1,1,1,1],[0,0,1,0],[0,1,0,0],[1,1,1,1]]
  zero = [[0,1,0],[1,0,1],[1,0,1],[0,1,0]]
  one = [[0,1,0],[1,1,0],[0,1,0],[1,1,1]]
  two = [[0,1,0],[1,0,1],[0,1,0],[1,1,1]]
  three = [[1,1,1,0],[0,1,1,0],[0,1,1,0],[1,1,1,0]]
  four = [[0,0,1,0],[0,1,1,0],[1,1,1,1],[0,0,1,0]]
  five = [[1,1,1],[1,0,0],[0,1,1],[1,1,1]]
  six = [[0,1,1],[1,0,0],[1,1,1],[1,1,1]]
  seven = [[1,1,1],[0,0,1],[0,0,1],[0,0,1]]
  eight = [[0,1,1],[0,1,1],[1,1,0],[1,1,0]]
  nine = [[1,1,1],[1,1,1],[0,0,1],[1,1,0]]
  fullstop = [[0],[0],[0],[1]]
  space = [[0,0],[0,0],[0,0],[0,0]]
  apostrophe = [[1],[0],[0],[0]]
  bang = [[1],[1],[0],[1]]
  question = [[1,1,1],[0,1,1],[0,0,0],[0,1,0]]
  colon = [[0],[1],[0],[1]]
  semicolon = [[0,1],[0,0],[0,1],[1,0]]
  unknown = [[0,0],[1,1],[1,1],[0,0]]
  glyphMap = { 'unknown':unknown, '0':zero, '1':one, '2':two, '3':three, '4':four, '5':five, '6':six, '7':seven, '8':eight, '9':nine, 'a':a, 'b':b, 'c':c, 'd':d, 'e':e, 'f':f, 'g':g, 'h':h, 'i':i, 'j':j, 'k':k, 'l':l, 'm':m, 'n':n, 'o':o, 'p':p, 'q':q, 'r':r, 's':s, 't':t, 'u':u, 'v':v, 'w':w, 'x':x, 'y':y, 'z':z, 'A':a, 'B':b, 'C':c, 'D':d, 'E':e, 'F':f, 'G':g, 'H':h, 'I':i, 'J':j, 'K':k, 'L':l, 'M':m, 'N':n, 'O':o, 'P':p, 'Q':q, 'R':r, 'S':s, 'T':t, 'U':u, 'V':v, 'W':w, 'X':x, 'Y':y, 'Z':z, '.':fullstop, ' ':space, '\'':apostrophe, '!':bang, '?':question, ':':colon, ';':semicolon }

class MessageService:
  def GET(self, message):
    global display
    print (self)
    if not message:
      message = 'ERR: No message set'
    display.setMessage(message)
    return 'OK'

if __name__ == "__main__":
  display = UnicornDisplay()
  display.start()

  urls = ('/(.*)', 'MessageService')
  app = web.application(urls, globals())
  app.run()
