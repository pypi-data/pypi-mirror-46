# -*- coding: utf-8 -*-
import time
import sys
import quamash
import asyncio
import imageio
import numpy as np
import glob
from natsort import natsorted
import multiprocessing

from qtpy import QtGui, QtCore, QtWidgets
from qimage2ndarray import array2qimage
from clickpoints.includes.qextendedgraphicsview import QExtendedGraphicsView
from queue import Queue, Empty
from threading import Thread
from functools import partial
from concurrent.futures import ProcessPoolExecutor



class TiledPixmapItem(QtWidgets.QGraphicsPixmapItem):
    conversion = None
    max_value = 256

    max_image_size = 256

    def __init__(self, *args):
        super().__init__(*args)
        self.pixmaps = []

    def updateCount(self, number):
        if len(self.pixmaps) < number:
            for i in range(number-len(self.pixmaps)):
                pixmap = QtWidgets.QGraphicsPixmapItem(self)
                self.pixmaps.append(pixmap)
        else:
            for i in range(len(self.pixmaps) - number):
                pixmap = self.pixmaps.pop()
                pixmap.scene().removeItem(pixmap)

    def setImage(self, image):
        # get number of tiles
        self.number_of_imagesX = int(np.ceil(image.shape[1] / self.max_image_size))
        self.number_of_imagesY = int(np.ceil(image.shape[0] / self.max_image_size))

        # iterate over tiles
        for y in range(self.number_of_imagesY):
            for x in range(self.number_of_imagesX):
                # determine tile region
                i = y * self.number_of_imagesX + x
                start_x = x * self.max_image_size
                start_y = y * self.max_image_size
                end_x = min([(x + 1) * self.max_image_size, image.shape[1]])
                end_y = min([(y + 1) * self.max_image_size, image.shape[0]])
                # retrieve image slice and convert it to qimage
                slice = image[start_y:end_y, start_x:end_x, :]
                qimage = array2qimage(slice)
                # set the offset for the tile
                self.pixmaps[i].setOffset(start_x, start_y)
                self.pixmaps[i].setScale(1)
                # store that we want to show that tile
                self.pixmaps[i].setPixmap(QtGui.QPixmap(qimage))

    def setImageFirstTime(self, image):
        # set image called for the first time, therefore, we set a conversion if none is set
        if image.dtype == np.uint16:
            if image.max() < 2**12:
                self.max_value = 2**12
            else:
                self.max_value = 2**16
            self.setConversion(generateLUT(0, self.max_value, 1, 2**16))
        else:
            self.setImage = self.setImageDirect
        self.setImage(image)

    def setImageDirect(self, image):
        self.setPixmap(QtGui.QPixmap(array2qimage(image.astype(np.uint8))))

    def setImageLUT(self, image):
        self.setPixmap(QtGui.QPixmap(array2qimage(self.conversion[image[:, :, :3]])))

    def setConversion(self, conversion):
        self.conversion = conversion
        if isinstance(conversion, np.ndarray):
            self.setImage = self.setImageLUT
        else:
            self.setImage = self.setImageDirect


class ImageReader:
    def __call__(self, filename):
        return imageio.imread(filename)

class ImageLoadThreadPool:
    def __init__(self, loop: asyncio.AbstractEventLoop, count=10):
        self._threads = [ImageConnection(loop) for i in range(count)]
        for t in self._threads:
            t.start()

    async def imread(self, filename) -> None:
        """Commit the current transaction."""
        while True:
            for thread in self._threads:
                if not thread.busy:
                    thread.busy = True
                    image = await thread.imread(filename)
                    thread.busy = False
                    return image
            await asyncio.sleep(0)

class ImageConnection(Thread):
    busy = False

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        super().__init__()
        self._running = True
        self._connection = None  # type: Optional[sqlite3.Connection]
        self._loop = loop
        self._tx = Queue()  # type: Queue

    def run(self) -> None:
        """Execute function calls on a separate thread."""
        while self._running:
            try:
                future, function = self._tx.get(timeout=0.1)
                print("quueu get")
            except Empty:
                continue

            try:
                #LOG.debug("executing %s", function)
                result = function()
                #LOG.debug("returning %s", result)
                self._loop.call_soon_threadsafe(future.set_result, result)
            except BaseException as e:
                #LOG.exception("returning exception %s", e)
                self._loop.call_soon_threadsafe(future.set_exception, e)

    async def _execute(self, fn, *args, **kwargs):
        """Queue a function with the given arguments for execution."""
        function = partial(fn, *args, **kwargs)
        future = self._loop.create_future()

        self._tx.put_nowait((future, function))

        return await future

    def __await__(self):
        self.start()
        return self._connect().__await__()

    async def __aenter__(self) -> "Connection":
        return await self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def imread(self, filename) -> None:
        """Commit the current transaction."""
        return await self._execute(imageio.imread, filename)


def array2qimage(a):
    if a.shape[2] == 3:
        return QtGui.QImage(a, a.shape[1], a.shape[0], QtGui.QImage.Format_RGB888)
    im = QtGui.QImage(a, a.shape[1], a.shape[0], QtGui.QImage.Format_Grayscale8)
    return im

def generateLUT(min, max, gamma, bins):
    if min >= max:
        min = max-1
    if min < 0:
        min = 0
    if max >= bins:
        max = bins-1
    if max <= min:
        max = min+1
    dynamic_range = max - min
    conversion = np.arange(0, int(bins), dtype=np.uint8)
    conversion[:min] = 0
    conversion[min:max] = np.power(np.linspace(0, 1, dynamic_range, endpoint=False), gamma) * 255
    conversion[max:] = 255
    return conversion

class ClickPointsWindow(QtWidgets.QWidget):

    def __init__(self, path, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)

        # window layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.start_stop_button = QtWidgets.QPushButton("start")
        self.start_stop_button.clicked.connect(self.start_stop)
        self.layout.addWidget(self.start_stop_button)

        self.fps_label = QtWidgets.QLabel()
        self.layout.addWidget(self.fps_label)

        # view/scene setup
        self.view = QExtendedGraphicsView.QExtendedGraphicsView()
        self.origin = self.view.origin
        self.layout.addWidget(self.view)

        self.pixmap = QtWidgets.QGraphicsPixmapItem(self.origin)

        self.images = natsorted(glob.glob(path))
        self.image_index = 0

        self.running = True
        asyncio.ensure_future(self.newImage(), loop=loop)

        self.reader = ImageReader()
        self.pool = multiprocessing.Pool()

        self.lut = generateLUT(0, 2**16, 1, 2**16)
        self.last_pixmap = None

        self.connection = ImageLoadThreadPool(loop)
        #self.connection.start()

    def start_stop(self):
        self.running = not self.running

    async def readImage(self, filename):
        return await self.connection.imread(filename)
        return imageio.imread(filename)
        #return self.pool.map(self.reader, [filename])[0]
        return await loop.run_in_executor(None, imageio.imread, filename)

    async def processImage(self, image):
        return image#self.lut[image]#/255

    async def pixmapImage(self, image):
        return QtGui.QPixmap(array2qimage(image))

    async def loadImage(self, index):
        index = index % len(self.images)

        try:
            im = await self.readImage(self.images[index])
        except (ValueError, SyntaxError):
            im = np.zeros((100, 100, 3), dtype=np.uint8)
        im = await self.processImage(im)
        pixmap = await self.pixmapImage(im)

        #im = imageio.imread(self.images[index])/255
        #im = self.pool.map(self.reader, [self.images[index]])[0]
        #pixmap = QtGui.QPixmap(array2qimage(im.astype(np.uint8)))
        return pixmap, [im.shape[1], im.shape[0]]

    def displayImage(self, pixmap, extent):
        self.pixmap.setPixmap(pixmap)
        self.view.setExtend(*extent)

    async def newImage(self):
        t = time.time()
        target_fps = 6
        target_delta_t = 1/target_fps
        last_overhead = 0
        mean_delta_t = target_delta_t
        averaging_decay = 0.9
        while True:
            if self.running:
                # load the image and wait for the timeout to occur
                pixmap, extent = await self.loadImage(self.image_index)

                print("wait time", max((t + target_delta_t) - time.time(), 0))
                await asyncio.sleep(max((t + target_delta_t) - time.time(), 0))
                display_time = time.time()
                # display the image
                self.displayImage(pixmap, extent)
                # go to the next image
                self.image_index += 1
                if 0 and self.image_index == 20:#len(self.images):
                    print("Total time", time.time()-time_start)
                    self.close()

                # calculate the time slip
                delta_t = time.time()-t
                t = time.time()

                mean_delta_t = averaging_decay * mean_delta_t + (1 - averaging_decay) * delta_t
                print("%.1f" % (1 / mean_delta_t), delta_t)
                self.fps_label.setText(
                    "%.1ffps %s" % (1 / mean_delta_t, self.images[self.image_index % len(self.images)]))
            else:
                await asyncio.sleep(0.01)
                t = time.time()

    async def newImage(self):
        t = time.time()
        target_fps = 12
        target_delta_t = 1/target_fps
        last_overhead = 0
        mean_delta_t = target_delta_t
        averaging_decay = 0.9

        image_tasks = [None]*len(self.images)
        while True:
            if self.running:
                for i in range(5):
                    index = (self.image_index+i) % len(self.images)
                    if image_tasks[index] is None:
                        image_tasks[index] = loop.create_task(self.loadImage(index))

                # load the image and wait for the timeout to occur
                pixmap, extent = await image_tasks[self.image_index]
                image_tasks[self.image_index] = None
                print("wait time", time.time()-(t+target_delta_t))
                #await asyncio.sleep(max(time.time()-(t+target_delta_t), 0))
                await asyncio.sleep(target_delta_t)
                #(pixmap, extent), _ = await asyncio.gather(image_tasks[self.image_index], asyncio.sleep(target_delta_t-last_overhead))
                # display the image
                self.displayImage(pixmap, extent)
                # go to the next image
                self.image_index = (self.image_index + 1) % len(self.images)

                # calculate the time slip
                delta_t = time.time()-t + 0.000001
                t = time.time()
                last_overhead += 0.1*(delta_t - target_delta_t)

                mean_delta_t = averaging_decay*mean_delta_t + (1-averaging_decay)*delta_t
                print("%.1f" % (1/mean_delta_t), last_overhead, delta_t)
                self.fps_label.setText("%.1ffps %s" % (1/mean_delta_t, self.images[self.image_index % len(self.images)]))
            else:
                await asyncio.sleep(0.01)
                t = time.time()

time_start = time.time()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    loop = quamash.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # init and open the ClickPoints window
    with loop:
        #window = ClickPointsWindow("D:\TestData\Cardiomyocytes3\*.tif")
        #window = ClickPointsWindow(r"D:\TestData\test-images-new-camera\*.tif")
        window = ClickPointsWindow(r"D:\2013-04-17\*_Crozet_GoPro.jpg")
        window.show()
        loop.run_forever()
        print("end")
