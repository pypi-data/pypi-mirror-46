from simple_pyueye.camera import *
from threading import Thread
import cv2 as cv


def still_capture(camID=1):
    camera = CameraObj(camID)
    camera.open()
    camera.capture_still()
    camera.close()


class ImageProcess:
    def __init__(self):
        self.type = 'None'
        self.emboss_filter = np.array([[-2, 1, 0], [-1, 1, 1], [0, 1, 2]])

    def filter(self, img, normalize=False):
        if self.type == 'None':
            pass
        elif self.type == 'laplacian':
            img = cv.Laplacian(img, cv.CV_64F, 7)
        elif self.type == 'emboss':
            img = cv.filter2D(img, cv.CV_8U, self.emboss_filter)
        elif self.type == 'invert':
            img = np.abs(img.astype(np.int) - 255)
        if normalize:
            img = self.normalize(img)
        return img.clip(0, 255).astype(np.uint8)

    def normalize(self, img):
        return ((img - img.min()) / (img.max() - img.min())) * 255


def continuous_capture_filters(camera):
    if camera.mem.__len__() == 0:
        warnings.warn('Warning: Memory not allocated! Allocating memory to default AOI...')
        camera.alloc_mem()

    if camera.EventHandler.__len__() == 0:
        warnings.warn('Warning: Frame Event not installed! Installing...')
        camera.install_event(u.IS_FRAME)

        camera.capture = True
    check(u.is_CaptureVideo(camera.id, u.IS_WAIT))

    ip = ImageProcess()
    while camera.capture:
        mem = ImageBuffer()
        we.WaitForSingleObject(camera.EventHandler[0], we.INFINITE)
        check(u.is_GetActiveImageMem(camera.id, mem.ptr, mem.id))
        check(u.is_CopyImageMem(camera.id, mem.ptr, mem.id, camera.currContainer.ctypes.data))
        check(u.is_UnlockSeqBuf(camera.id, mem.id, mem.ptr))

        """Place further processing code here
            Image is placed in self currContainer"""

        play = ip.filter(camera.currContainer)
        size = cv.getTextSize('Press q to exit', cv.FONT_HERSHEY_SIMPLEX, 1, 1)
        cv.rectangle(play, (10, 50 - size[0][1]), (10 + size[0][0], 50 + size[1]), (0, 0, 0),
                     thickness=cv.FILLED)
        cv.putText(play, 'Press q to exit', (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                   thickness=1)

        key = cv.waitKey(1)
        if key == ord('q'):
            camera.capture = False
        elif key == ord('l'):
            ip.type = 'laplacian'
        elif key == ord('e'):
            ip.type = 'emboss'
        elif key == ord('n'):
            ip.type = 'None'
        elif key == ord('i'):
            ip.type = 'invert'

        # play = (((play - play.min()) / (play.max() - play.min())) * 255).astype(np.uint8)
        cv.imshow('Live', play)
    camera.stop_live_video()


def continuous_capture(camID=1):
    camera = CameraObj(camID)
    camera.open()
    # camera.set_color_mode(u.IS_CM_MONO8)
    t = Thread(target=continuous_capture_filters, args=(camera,))
    t.start()
    t.join()
    camera.close()
