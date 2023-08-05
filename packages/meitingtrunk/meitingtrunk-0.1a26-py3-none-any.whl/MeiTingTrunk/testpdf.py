import sys
import os
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QUrl

#PDFJS = 'file:///path/to/pdfjs-1.9.426-dist/web/viewer.html'
# PDFJS = 'file:///usr/share/pdf.js/web/viewer.html'
#PDFJS = 'file:///home/guangzhi/codes/MeiTingTrunk/MeiTingTrunk/lib/pdfjs/web/viewer.html'
PDFJS = './lib/pdfjs/web/viewer.html'
#PDF = 'file:///home/guangzhi/codes/MeiTingTrunk/MeiTingTrunk/samples/sample_pdf3.pdf'
PDF = './samples/sample_pdf3.pdf'

def getPath(relpath):

    if not os.path.isabs(relpath):
        p=os.path.abspath(relpath)
    else:
        p=relpath

    p=QUrl.fromLocalFile(p).toString()
    return p


class Window(QtWebEngineWidgets.QWebEngineView):
    def __init__(self):
        super(Window, self).__init__()
        pdfjs_path=getPath(PDFJS)
        pdf_path=getPath(PDF)

        print(pdfjs_path)
        print(pdf_path)
        #print(os.path.exists(pdfjs_path))
        #print(os.path.exists(pdf_path))
        aa='%s?file=%s' %(pdfjs_path, pdf_path)
        print('aa=',aa)
        bb=QUrl.fromUserInput(aa)
        print('bb=',bb)
        self.load(bb)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(600, 50, 800, 600)
    window.show()
    sys.exit(app.exec_())
