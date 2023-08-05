#!/usr/bin/env python2.7
#coding:utf-8


#import bpy
import os
import shutil

import math
import random
from PIL import Image
import time

import codecs
import hjson

from bslideshow.director import Director
from bslideshow.slideshow import Slideshow
from bslideshow.tools import BlenderTools

class Project(object):

  def __init__ (self, path):
    cwd = os.getcwd()
    if path is not None and not os.path.isabs(path):
      path = os.path.join(cwd, path)
    self.path = path
    self.parents = []

  def generateMainSection (self, section):
    print("generate Main Section " + section['title'])
    sectTitle = self.generateTitleSection(section)
    outSections = list()
    for simpleSection in section['sections']:
      self.parents.append([simpleSection, section])
      outSection = self.generateSection(simpleSection)
      outSections.append(outSection)
    sectContent = self.mergeWithTransitions(section, outSections)
    print("sectContent = " + str(sectContent))

    tools = BlenderTools()

    print("sectTitle = " + sectTitle)
    sectionTitleFadeIn = os.path.join(os.path.dirname(self.path), section['path'] + "_title_fadeIn" + ".mp4")
    if not os.path.isfile(sectionTitleFadeIn):
      tools.fadeIn(moviePath=str(sectTitle), duration=48, movieOutput=str(sectionTitleFadeIn))
    print("sectionTitleFadeIn = " + sectionTitleFadeIn)
    sectionTitleFadeOut = os.path.join(os.path.dirname(self.path), section['path'] + "_title_fadeOut" + ".mp4")
    if not os.path.isfile(sectionTitleFadeOut):
      tools.fadeOut(moviePath=str(sectionTitleFadeIn), duration=48, movieOutput=str(sectionTitleFadeOut))
    print("sectionTitleFadeOut = " + sectionTitleFadeOut)

    sectionContentFadeIn = os.path.join(os.path.dirname(self.path), section['path'] + "_fadeIn" + ".mp4")
    if not os.path.isfile(sectionContentFadeIn):
      tools.fadeIn(moviePath=str(sectContent), duration=48, movieOutput=str(sectionContentFadeIn))
    print("sectionContentFadeIn = " + sectionContentFadeIn)
    sectionContentFadeOut = os.path.join(os.path.dirname(self.path), section['path'] + "_fadeOut" + ".mp4")
    if not os.path.isfile(sectionContentFadeOut):
      tools.fadeOut(moviePath=str(sectionContentFadeIn), duration=48, movieOutput=str(sectionContentFadeOut))
    print("sectionContentFadeOut = " + sectionContentFadeOut)

    sectionMain = os.path.join(os.path.dirname(self.path), section['path'] + "" + ".mp4")
    if not os.path.isfile(sectionMain):
      tools.merge(movie1Path=str(sectionTitleFadeOut), movie2Path=str(sectionContentFadeOut), movieOutput=str(sectionMain))

    result = sectionMain
    print("mainSection = " + sectionMain)

    return result

  def generateTitleSection (self, section):
    result = None

    print("generate Title Section " + section['title'])

    sectionTitle = os.path.join(os.path.dirname(self.path), section['path'] + "_title.mp4") if 'path' in section else os.path.join(os.path.dirname(self.path), "title.mp4")
    print("sectionTitle generate Title Section " + sectionTitle)
    if not os.path.isfile(sectionTitle):
      director = Director()
      director.runMode = 'LOW'
      #director.maxDebugFrames = 9999999
      director.frame_step = 1
      pathFolderTitle = self.selectTitleFolder(section)
      print("pathFolderTitle = " + pathFolderTitle)
      director.animSceneTitle(str(pathFolderTitle), movieOutput=str(sectionTitle))
      print("out section = " + sectionTitle)
    result = sectionTitle
    return result

  def selectTitleFolder (self, section, size=16):
    result = None

    sectionPath = section['path'] if 'path' in section else self.path
    sections = section['sections'] if 'path' in section else self.loadAllSubsections(section)

    result = os.path.join(os.path.dirname(self.path), sectionPath + "_title_folder") if 'path' in section else os.path.join(os.path.dirname(self.path), "title_folder")
    if not os.path.isdir(result):
      os.mkdir(result)

      for i in range(size):
        subsection = random.choice(sections)
        folderSubsection = os.path.join(os.path.dirname(self.path), subsection['path'])
        imagesSubsection = [os.path.join(folderSubsection, f) for f in os.listdir(folderSubsection) if (f.lower().endswith('.jpg') or f.lower().endswith('.png')) and os.path.isfile(os.path.join(folderSubsection, f))]
        selectedImg = random.choice(imagesSubsection)
        filename, fextension = os.path.splitext(os.path.basename(selectedImg))
        shutil.copyfile(selectedImg, os.path.join(result, filename + '_' + str(i) + fextension))

    return result

  def loadAllSubsections (self, section):
    result = list()
    for item in section['sections']:
      result.extend(item['sections'])
    return result

  def mergeWithTransitions (self, section, sections=None):
    result = None
    print("mergeWithTransitions " + section['title'])

    pathSection = os.path.join(os.path.dirname(self.path), section['path'] + "_transitions" + ".mp4") if 'path' in section else os.path.join(os.path.dirname(self.path), os.path.splitext(os.path.basename(self.path))[0] + "_transitions" + ".mp4")

    tools = BlenderTools()
    tools.runMode = 'LOW'
    tools.frame_step = 1

    if not os.path.isfile(pathSection):
      transitions = ['transition41.mp4', 'transition45.mp4', 'transition48.mp4', 'transition80.mp4', 'transition90.mp4']
      for item in sections:
        if result is None:
          result = pathSection
          shutil.copyfile(item, pathSection)
        else:
          tools.doAddTransition(movie1Path=str(pathSection), movie2Path=str(item), transitionPath=str(random.choice(transitions)), movieOutput=str(pathSection))

    result = pathSection

    return result

  def generateSection (self, section):
    result = None

    print("generate Section " + section['title'])
    director = Director()
    director.runMode = 'LOW'
    #director.maxDebugFrames = 9999999
    director.frame_step = 1
    pathSection = os.path.join(os.path.dirname(self.path), section['path'])

    sectionBase = os.path.join(os.path.dirname(self.path), section['path'] + "_base" + ".mp4")
    print("path section = " + pathSection)
    if not os.path.isfile(sectionBase):
      director.animScene(str(pathSection), movieOutput=str(sectionBase))
    print("out section = " + sectionBase)

    foregroundPath = 'overlay22.mp4'
    tools = BlenderTools()
    tools.runMode = 'LOW'
    #tools.maxDebugFrames = 99
    tools.frame_step = 1
    #tools.maxDebugFrames = 24

    sectionForeground = os.path.join(os.path.dirname(self.path), section['path'] + "_foreground" + ".mp4")
    if not os.path.isfile(sectionForeground):
      tools.addForeground(str(sectionBase), foregroundPath, movieOutput=str(sectionForeground))
    print("out2 section = " + sectionForeground)


    #tools.maxDebugFrames = 24
    sectionBanner = os.path.join(os.path.dirname(self.path), section['path'] + "_banner" + ".mp4")
    if not os.path.isfile(sectionBanner):
      print("generating banner")
      print("type title = " + str(type(section['title'])))
      tools.generateBanner(title = str(section['title']), subtitle = str(section['subtitle']), movieOutput=str(sectionBanner))
    print("banner section = " + sectionBanner)

    sectionBannerOffset = os.path.join(os.path.dirname(self.path), section['path'] + "_bannerOffset" + ".mp4")
    if not os.path.isfile(sectionBannerOffset):
      tools.addOffset(str(sectionBanner), framesOffset = 48, movieOutput=str(sectionBannerOffset))
    #bannerOffset = '/tmp/.movieRWAuLJ.mp4'
    print("bannerOffset section = " + sectionBannerOffset)


    sectionResult = os.path.join(os.path.dirname(self.path), section['path'] + "" + ".mp4")
    if not os.path.isfile(sectionResult):
      tools.doAddBanner(str(sectionForeground), str(sectionBannerOffset), movieOutput=str(sectionResult))
    print("result section = " + sectionResult)

    result = sectionResult
    return result

  def __saveObj__ (self, path, obj):
    fp = codecs.open(path, mode='w', encoding='utf-8')
    hjson.dump(obj, fp)

  def __loadObj__ (self, path):
    result = None
    fp = codecs.open(path, mode='r', encoding='utf-8')
    result = hjson.load(fp)
    return result

  def __get_parent__ (self, data):
    result = None
    for item in self.parents:
      if data == item[0]:
        result = item[1]
        break
    return result

  def generate (self):
    result = None
    data = self.__loadObj__(self.path)
    self.parents.append([data, None])
    self.generateTitleSection(data)
    outSections = list()
    for mainSection in data['sections']:
      self.parents.append([mainSection, data])
      outSection = self.generateMainSection(mainSection)
      outSections.append(outSection)
    self.mergeWithTransitions(data, outSections)
    return result





if __name__ == '__main__':
  p = Project("/home/jmramoss/hd/res_slideshow/project/myproject.hjson")
  #Green screen https://www.youtube.com/watch?v=jw8a_9OfVN8
  #p.generate()
  #tools = BlenderTools()
  #tools.runMode = 'LOW'
  #tools.split(moviePath='/home/jmramoss/hd/res_slideshow/project/test.mp4', frameStart=1, frameEnd=4*96, movieOutput='/home/jmramoss/hd/res_slideshow/project/test_split.mp4')
  #tools.fadeIn(moviePath='/home/jmramoss/hd/res_slideshow/project/test_split.mp4', duration=96, movieOutput='/home/jmramoss/hd/res_slideshow/project/test_fadeIn2.mp4')
  #tools.fadeOut(moviePath='/home/jmramoss/hd/res_slideshow/project/test_fadeIn2.mp4', duration=96, movieOutput='/home/jmramoss/hd/res_slideshow/project/test_fadeOut2.mp4')
  #tools.merge(movie1Path='/home/jmramoss/hd/res_slideshow/project/test_fadeIn2.mp4', movie2Path='/home/jmramoss/hd/res_slideshow/project/test_fadeOut2.mp4', movieOutput='/home/jmramoss/hd/res_slideshow/project/test_merge.mp4')
  #p.mergeWithTransitions(None, ["/tmp/.movie8p71ol.mp4", "/tmp/.moviehkqFpL.mp4", "/tmp/.movie5H4coh.mp4"])
  #p.generateTitleSection(p.sections[0])
  p.generate()


