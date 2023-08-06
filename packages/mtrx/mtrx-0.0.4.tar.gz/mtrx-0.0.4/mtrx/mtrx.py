import pyqrcode, os, sys


def Qrcode(text, Format):
    pyqrcode.create('%s'%text).svg('%s.%s'%(text, Format), scale=8)
