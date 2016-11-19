#!/usr/bin/env python

import unicornhat as unicorn
import time
import numpy as np
import web
import threading

from datetime import datetime as dt
import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta

import feedparser

class UnicornDisplay:
  unicorn.set_layout(unicorn.AUTO)
  unicorn.rotation(180)
  unicorn.brightness(1.0)
  screenWidth,screenHeight=unicorn.get_shape()

  BAR_DATUM_LENGTH = 0
  BAR_DATUM_RED = 1
  BAR_DATUM_GREEN = 2
  BAR_DATUM_BLUE = 3
  barData = [[0,0,0,0],[0,0,0,0], [0,0,0,0], [0,0,0,0]]

  glyphHeight = 4
  glyphSpacing = 1
  scrollXOffset = -screenWidth
  message = ""
  messageColour = [120, 90, 50]
  messagePixels = np.zeros((1, glyphHeight), dtype=np.bool)
  displayType = 'message'

  def start(self):
    t = threading.Thread(target=self.loopMessage)
    t.daemon = True
    t.start()

  def setBar(self, row, displayInfo):
    self.barData[row] = displayInfo 

  def loopMessage(self):
    print('Display loop started.')
    global scrollXOffset
    scrollXOffset = -self.screenWidth
    while True:
      unicorn.clear()
      if self.displayType == 'message':
        for screenx in range(self.screenWidth):
          for screeny in range(self.screenHeight):
            screenxOffset = screenx + scrollXOffset
            if (screenxOffset >= 0) and (screenxOffset < len(self.messagePixels)) and (self.messagePixels[screenxOffset][screeny]):
              unicorn.set_pixel(screenx, screeny, self.messageColour[0], self.messageColour[1], self.messageColour[2])
        unicorn.show()
        scrollXOffset += 1
        if scrollXOffset > len(self.messagePixels):
          scrollXOffset = -self.screenWidth 
        time.sleep(0.05)
      elif self.displayType == 'bar':
   
        for screeny in range(self.screenHeight):
          for screenx in range(self.screenWidth):
            if screenx < self.barData[screeny][self.BAR_DATUM_LENGTH]:
              unicorn.set_pixel(screenx, screeny, self.barData[screeny][self.BAR_DATUM_RED], self.barData[screeny][self.BAR_DATUM_GREEN], self.barData[screeny][self.BAR_DATUM_BLUE])
          
        unicorn.show()

  def setMessage(self, message, **kwargs):
    print('Display message received: ' + message)

    colour = kwargs.get('colour', None)
    if colour is not None:
      self.messageColour = colour
    else:
      self.messageColour = [90, 70, 50]

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
  hyphen = [[0,0,0],[0,0,0],[1,1,1],[0,0,0]]
  unknown = [[0,0],[1,1],[1,1],[0,0]]
  glyphMap = { 'unknown':unknown, '0':zero, '1':one, '2':two, '3':three, '4':four, '5':five, '6':six, '7':seven, '8':eight, '9':nine, 'a':a, 'b':b, 'c':c, 'd':d, 'e':e, 'f':f, 'g':g, 'h':h, 'i':i, 'j':j, 'k':k, 'l':l, 'm':m, 'n':n, 'o':o, 'p':p, 'q':q, 'r':r, 's':s, 't':t, 'u':u, 'v':v, 'w':w, 'x':x, 'y':y, 'z':z, 'A':a, 'B':b, 'C':c, 'D':d, 'E':e, 'F':f, 'G':g, 'H':h, 'I':i, 'J':j, 'K':k, 'L':l, 'M':m, 'N':n, 'O':o, 'P':p, 'Q':q, 'R':r, 'S':s, 'T':t, 'U':u, 'V':v, 'W':w, 'X':x, 'Y':y, 'Z':z, '.':fullstop, ' ':space, '\'':apostrophe, '!':bang, '?':question, ':':colon, ';':semicolon, '-':hyphen }

class WebMessageService:
  def GET(self, message):
    global display
    print (self)
    if not message:
      message = 'ERR: No message set'
    display.setMessage(message)
    return 'OK'

class MessageService:

  rssUrl = 'https://www.reddit.com/r/worldnews/top/.rss'
  feedTitles = []
  anniversaries = [("28 nov", "Bill's Birthday",0), ("1 jan","Bob's Birthday",0)]
  anniversariesToDisplay = []
  nextAnniversaryMessage = ''

  def start(self):
    global display
    display.displayType = 'message'

    t = threading.Thread(target=self.mainLoop)
    t.daemon = True
    t.start()

  def mainLoop(self):
    global display

    while True:
      self.updateCalendarDisplayInfo()
      self.updateFeedDisplayInfo()
      self.displayFeedInfo()

      if len(self.feedTitles) == 1:
        # Feed update error, try again in 3 minutes
        secondsToNextUpdate = 180
      else:
        secondsToNextUpdate = 3600

      secondsSinceDisplayModeChanged = 0
      DISPLAYMODE_ANNIVERSARY_BAR = 0
      DISPLAYMODE_ANNIVERSARY_MESSAGE = 1
      DISPLAYMODE_FEED = 2
      currentDisplayMode = DISPLAYMODE_FEED
      while secondsToNextUpdate > 0:
        time.sleep(1)
        secondsToNextUpdate -= 1
        secondsSinceDisplayModeChanged += 1

        if currentDisplayMode == DISPLAYMODE_FEED and secondsSinceDisplayModeChanged > 60:
          if len(self.anniversariesToDisplay) > 0:
            currentDisplayMode = DISPLAYMODE_ANNIVERSARY_BAR
            secondsSinceDisplayModeChanged = 0
            display.displayType = 'bar'
          else:
            # No calendar events, continue with feed mode
            secondsSinceDisplayModeChanged = 0

        elif currentDisplayMode == DISPLAYMODE_ANNIVERSARY_BAR and secondsSinceDisplayModeChanged > 4:
          currentDisplayMode = DISPLAYMODE_ANNIVERSARY_MESSAGE
          secondsSinceDisplayModeChanged = 0
          display.setMessage(self.nextAnniversaryMessage, colour=[255,69,0])
          display.displayType = 'message'

        elif currentDisplayMode == DISPLAYMODE_ANNIVERSARY_MESSAGE and secondsSinceDisplayModeChanged > 6:
          currentDisplayMode = DISPLAYMODE_FEED
          secondsSinceDisplayModeChanged = 0
          self.displayFeedInfo()

  def updateCalendarDisplayInfo(self):
    for i in range(0,3):
      display.setBar(i, [0,0,0,0])

    self.anniversariesToDisplay = self.getUpcoming()

    if len(self.anniversariesToDisplay) == 0:
      self.nextAnniversaryMessage = ''
    else:
      nextUpcoming = self.anniversariesToDisplay[0]
      self.nextAnniversaryMessage = nextUpcoming[1] + ' in ' + str(nextUpcoming[0]) + ' days'

      rowCount = 0
      for upcoming in self.anniversariesToDisplay:
        print(upcoming)
        if rowCount == 0:
          nextUpcoming = self.anniversariesToDisplay[0]
          # "Amy's birthday in 3 days"
          self.nextAnniversaryMessage = nextUpcoming[1] + ' in ' + str(nextUpcoming[0]) + ' days'
        display.setBar(rowCount, self.getBarDisplayInfo(upcoming))
        rowCount += 1

  def updateFeedDisplayInfo(self):
    try:
      feed = feedparser.parse(self.rssUrl)
      if len(feed.entries) > 0:
        self.feedTitles = [entry.title for entry in feed.entries]
      else:
        self.feedTitles = ['Empty feed']
    except Exception as e:
      print (e)
      self.feedTitles = ['Feed error ' + e]
      pass

  def displayFeedInfo(self):  
    display.setMessage(' - '.join(self.feedTitles[:10]))
    display.displayType = 'message'

  def getBarDisplayInfo(self, upcomingInfo):
    if upcomingInfo[2] == 0:
      colour = (50, 0, 0)
    elif upcomingInfo[2] == 1:
      colour = (0, 50, 0)
    else:
      colour = (0, 0, 50)

    return [upcomingInfo[0], colour[0], colour[1], colour[2]]

  def getUpcoming(self):
    return \
      (sorted([ ((self.parseFuture(anniversary[0]) - datetime.date.today()).days, anniversary[1], anniversary[2])
      for anniversary
      in self.anniversaries
      if ((self.parseFuture(anniversary[0]) - datetime.date.today()).days <= 8) ])) \
      [:4]

  def parseFuture(self, timestr):
    """Same as dateutil.parser.parse() but only returns future dates."""
    now = datetime.date.today()
    default = datetime.date.today()
    for _ in range(401):  # assume gregorian calendar repeats every 400 year
      try:
        dt = parser.parse(timestr, default=default)
      except ValueError:
        pass
      else:
        if dt > now: # found future date
          break
      default += relativedelta(years=+1)
    else: # future date not found
      raise ValueError('failed to find future date for %r' % (timestr,))
    return dt

if __name__ == "__main__":
  display = UnicornDisplay()
  display.start()

  cal = MessageService()
  cal.start()

  urls = ('/(.*)', 'WebMessageService')
  app = web.application(urls, globals())
  app.run()
