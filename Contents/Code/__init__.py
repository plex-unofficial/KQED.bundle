"""
Author: Pierre Della Nave 
Date: May 2009
Revision: 0.1

Acknowledgements and Credits:
"""

import re, urllib
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

PLUGIN_PREFIX           = "/video/KQED"
PLUGIN_ID               = "com.plexapp.plugins.KQED"
PLUGIN_REVISION         = 0.1
PLUGIN_UPDATES_ENABLED  = True

WEB_ROOT = 'http://www.kqed.org'

CACHE_INTERVAL = 3600 * 3

YAHOO_NAMESPACE  = {'media':'http://search.yahoo.com/mrss/'}
ITUNES_NAMESPACE  = {'itunes':'http://search.yahoo.com/mrss/'}

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, 'KQED', 'KQED_logo.jpg', 'KQED_background.jpg')
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = 'KQED'
  MediaContainer.content = 'Items'
  MediaContainer.art = R('KQED_background.jpg')
  HTTP.SetCacheTime(CACHE_INTERVAL)

####################################################################################################
def MainMenu():
  dir = MediaContainer(title1="KQED")
  #feedlist = ('http://blogs.kqed.org/food/feed/',
  feedlist = ('http://www.kqed.org/rss/questvideo.xml',
              'http://feeds.feedburner.com/KqedGalleryCrawl',
              'http://www.kqed.org/rss/private/spark.xml',
              'http://feeds.feedburner.com/KqedTrulyCaShorts')

  for feed in feedlist:
    title = get_program_title(feed)
    dir.Append(Function(DirectoryItem(get_content,title=title,thumb = get_program_thumb(feed)),feed=feed, Menutitle = title))

  return dir

####################################################################################################
def get_content(sender, feed, Menutitle):

  dir = MediaContainer(title1="", title2=Menutitle, replaceParent=False)

  page = XML.ElementFromURL(feed, cacheTime=1200, values=None)
  for tag in page.xpath("channel//item"):
    video = tag.xpath("enclosure")[0].get("url")
    title =  tag.xpath("title")[0].text
    summary =  tag.xpath("description")[0].text

    thumbstr = tag.xpath("media:thumbnail", namespaces = YAHOO_NAMESPACE)
    if thumbstr:
      thumb = thumbstr[0].get("url")
    else:
      thumb = ''
    dir.Append(VideoItem(video,title,'',summary,'',thumb))
  return dir

####################################################################################################
def get_program_title(feed):

  page = XML.ElementFromURL(feed, cacheTime=1200, values=None)
  return page.xpath("channel/title")[0].text

####################################################################################################
def get_program_thumb(feed):

  page = XML.ElementFromURL(feed, cacheTime=1200, values=None)
  path = page.xpath("channel/image/url")
  if path:
    thumb = path[0].text
  else:
    path = page.xpath("channel/itunes:image", namespaces=ITUNES_NAMESPACE)
    if path:
      thumb = path[0].get("href")
    else :
      thumb ='http://www.kqed.org/assets/img/video-audio/logo-checkplease-75x75.gif'
  return thumb

