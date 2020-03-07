import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from PyQt5.QtGui import QImage, QIcon, QPixmap, QPalette, QBrush, QColor, QFontDatabase, QFont, QPainter
from qgis.core import *

def addLabel(layout,flabel,ffont,fsize,fbold,fitalic,fcolor,frp,falign,fpx,fpy):
    ftext = QgsLayoutItemLabel(layout)
    ftext.setText(flabel)
    ftext.setFont(QFont(ffont, fsize,fbold,fitalic))
    ftext.setFontColor(QColor(fcolor))
    ftext.setReferencePoint(frp)
    ftext.setHAlign(falign)
    ftext.adjustSizeToText()#refpoint upper right
    layout.addLayoutItem(ftext)
    ftext.attemptMove(QgsLayoutPoint(fpx, fpy, QgsUnitTypes.LayoutMillimeters))
    return

def addImage(layout,fLabel,fpx,fpy,w,h):
    fImg = QgsLayoutItemPicture(layout)
    fImg.setPicturePath(fLabel)
    layout.addLayoutItem(fImg)
    fImg.attemptMove(QgsLayoutPoint(fpx, fpy, QgsUnitTypes.LayoutMillimeters))
    fImg.attemptResize(QgsLayoutSize(w,h, QgsUnitTypes.LayoutMillimeters))
    #fImg.setBlendMode(QPainter.CompositionMode.CompositionMode_Multiply)
    return

def addLabelSection(layout,flabel,ffont,fsize,fbold,fitalic,fcolor,frp,falign,fpx,fpy,w,h,fmode):
    ftext = QgsLayoutItemLabel(layout)
    ftext.setText(flabel)
    ftext.setFont(QFont(ffont, fsize,fbold,fitalic))
    ftext.setFontColor(QColor(fcolor))
    ftext.setReferencePoint(frp)
    ftext.setHAlign(falign)
    ftext.adjustSizeToText()
    ftext.attemptResize(QgsLayoutSize(w,h, QgsUnitTypes.LayoutMillimeters))
    ftext.setMode(fmode)
    layout.addLayoutItem(ftext)
    ftext.attemptMove(QgsLayoutPoint(fpx, fpy, QgsUnitTypes.LayoutMillimeters))
    return
