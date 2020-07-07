# import os, time

from wslink import register as exportRpc

from paraview.web import protocols as pv_protocols


class ParaViewLiteWebProxyManager(pv_protocols.ParaViewWebProxyManager):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.lineContext = None

  @exportRpc("pv.proxy.manager.create.reader")
  def open(self, relativePath):

    fileToLoad = []
    validPath = ''
    if type(relativePath) == list:
        for file in relativePath:
            validPath = self.getAbsolutePath(file)
            if validPath:
                fileToLoad.append(validPath)
    else:
        validPath = self.getAbsolutePath(relativePath)
        if validPath:
            fileToLoad.append(validPath)

    extension = validPath[validPath.rfind('.') + 1:]
    if extension == 'csv':
      import csv
      with open(validPath) as csvfile:
        cinemaReader = csv.reader(csvfile, delimiter=',')
        line = 0
        pathIdx = 0
        for row in cinemaReader:
            if line == 0:
                pathIdx = row.index('FILE')
            elif line == 1:
                directory = validPath[:validPath.rfind('/')+1]
                filePath = directory + row[pathIdx]
                super().open(filePath)
                break

            line += 1


