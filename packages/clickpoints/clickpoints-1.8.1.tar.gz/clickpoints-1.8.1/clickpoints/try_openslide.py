import sys
#print(sys.executable)
#sys.path.insert(0, r"D:\Repositories\openslide-win64-20171122\bin")
#for l in sys.path:
#    print(l)
import openslide
import numpy as np

from qtpy import QtGui, QtCore, QtWidgets
from qtpy.QtCore import Qt
import qtawesome as qta
from qimage2ndarray import array2qimage

from clickpoints.includes import QExtendedGraphicsView



class ClickPointsWindow(QtWidgets.QWidget):
    folderEditor = None
    optionEditor = None
    first_frame = 0

    load_thread = None
    data_file = None

    signal_jump = QtCore.Signal(int)
    signal_jumpTo = QtCore.Signal(int)
    signal_broadcast = QtCore.Signal(str, tuple)

    def __init__(self, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.setMinimumWidth(650)
        self.setMinimumHeight(400)
        self.setWindowTitle("ClickPoints")

        # add layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.view = QExtendedGraphicsView(dropTarget=self)
        self.layout.addWidget(self.view)
        self.view.zoomEvent = self.zoomEvent
        self.view.panEvent = self.panEvent
        #self.local_scene = self.view.scene
        self.origin = self.view.origin

        import imageio
        try:
            im = imageio.imread("D:\Repositories\ClickPointsExamples\OpenSlide\CMU-1\CMU-1-40x - 2010-01-12 13.24.05.vms")
        except ValueError:

            im = openslide.OpenSlide(r"D:\USB_Sicherungskopie_2019_01_11\Schatzi\output.tif")
            print(im.level_count)
            print(im.level_dimensions)
            print(im.dimensions)
            print(im.level_downsamples)
            print("===========================")
            im = openslide.OpenSlide(r"D:\USB_Sicherungskopie_2019_01_11\Schatzi\output2.tif")
            print(im.level_count)
            print(im.level_dimensions)
            print(im.dimensions)
            print(im.level_downsamples)
            print("===========================")
            #im = openslide.OpenSlide(r"panorama_20170804-120649.tif")
#                "D:\Repositories\ClickPointsExamples\OpenSlide\CMU-1\CMU-1-40x - 2010-01-12 13.24.05.vms")

        print(im.level_count)
        print(im.level_dimensions)
        print(im.dimensions)
        print(im.level_downsamples)
        print(im.get_best_level_for_downsample(50))
        print(np.array(im.read_region((100, 100), im.get_best_level_for_downsample(50), (500, 500))).shape)
        self.im = im

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.timeout)


        self.imageBack = QtWidgets.QGraphicsPixmapItem(self.origin)
        max_data = im.read_region((0, 0), im.level_count-1, im.level_dimensions[im.level_count-1])
        self.imageBack.setPixmap(QtGui.QPixmap(array2qimage(np.asarray(max_data))))
        self.imageBack.setScale(im.level_downsamples[-1])

        self.last_level = None

        self.image = QtWidgets.QGraphicsPixmapItem(self.origin)
        self.image.setZValue(10)

        self.view.setExtend(*self.im.dimensions)
        self.view.fitInView()
        #print("print", 1/self.view.getOriginScale())

    def zoomEvent(self, scale, point):
        print(1/scale)
        #if self.imageBack is None:
        #    self.imageBack = QtWidgets.QGraphicsPixmapItem(self.origin)
        #    self.imageBack.setZValue(1)
        #    self.updateImage(self.imageBack)
        #self.updateImage(self.image)
        self.update_timer.start(10)

    def panEvent(self, xoff, yoff):
        print("panning")
        #self.updateImage(self.image)
        self.update_timer.start(10)

    def timeout(self):
        print("here")
        self.updateImage(self.image)
        self.update_timer.stop()

    def updateImage(self, pixmap):
        preview_rect = np.array(self.view.GetExtend(True)).astype("int") + np.array([0, 0, 1, 1])
        for i in [0, 1]:
            if preview_rect[i] < 0:
                preview_rect[i] = 0
            if preview_rect[i+2]-preview_rect[i] > self.im.dimensions[i]:
                preview_rect[i + 2] = self.im.dimensions[i] + preview_rect[i]

        level = self.im.get_best_level_for_downsample(1/self.view.getOriginScale())
        #if level == self.last_level:
        #    return
        self.last_level = level
        downsample = self.im.level_downsamples[level]
        print("level", level)

        dimensions_downsampled = (np.array(preview_rect[2:4]) - np.array(preview_rect[:2]))/downsample
        data = np.asarray(self.im.read_region(preview_rect[0:2], level, dimensions_downsampled.astype("int")))
        #data.flags.writeable = True
        #data[:, 0:10, :2] = 0
        #data[0:10, :, :2] = 0
        #data[:, -10:, :2] = 0
        #data[-10:, :, :2] = 0
        #print(data)
        #self.view.e
        pixmap.setPixmap(QtGui.QPixmap(array2qimage(data)))
        pixmap.setOffset(*(np.array(preview_rect[0:2])/downsample))
        pixmap.setScale(downsample)

    def keyPressEvent(self, event):
        print(event)
        if event.key() == QtCore.Qt.Key_F:
            print("update4")
            self.updateImage(self.image)


app = QtWidgets.QApplication(sys.argv)

# set an application id, so that windows properly stacks them in the task bar
if sys.platform[:3] == 'win':
    import ctypes
    myappid = 'fabrybiophysics.clickpoints'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# init and open the ClickPoints window
window = ClickPointsWindow()
window.show()
app.exec_()