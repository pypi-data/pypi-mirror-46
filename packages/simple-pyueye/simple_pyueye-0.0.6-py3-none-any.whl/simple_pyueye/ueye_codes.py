import numpy as np
from pyueye import ueye as u
import simple_pyueye
import os
from simple_pyueye.error_codes import ErrorCodes
from time import asctime

error_path = simple_pyueye.__file__
err = os.path.sep.join(error_path.split(os.path.sep)[:-1])


class Logger:
    def __init__(self, fp, text=None):
        self.text = text
        self.fp = fp

    def log(self, code):
        with open(self.fp, 'a') as f:
            f.write(str(code) + '\n')


def check(command, logger=None, log=None):
    nRet = command
    if nRet != 0:
        string, description = uEyeError().call(nRet)
        if logger is not None:
            if logger.text is not None:
                logger.log(logger.text)
            elif log is None:
                logger.log('{}\n{}, {}, {}\n'.format(asctime(), nRet, string, description))
            else:
                logger.log(log)
        raise uEyeException(string, description)


class uEyeException(Exception):
    def __init__(self, string, description):
        self.string = string
        self.description = description

    def __str__(self):
        return "Error: {} \nDescription: {}".format(self.string, self.description)


class uEyeError:
    # def __init__(self):
    #     filename = err + '\\error_codes.txt'
    #     error_str = list()
    #     error_description = list()
    #     error_no = list()
    #     f = open(filename, 'r')
    #     for line in f:
    #         val = line.split(';')
    #         error_no.append(int(val[0]))
    #         error_str.append(val[1])
    #         error_description.append(val[2])
    #     error_no = np.array(error_no)
    #     self.error_no = error_no
    #     self.error_str = error_str
    #     self.error_description = error_description

    def call(self, err_no):
        # arg = int(np.argwhere(self.error_no == err_no))
        # string = self.error_str[arg]
        string = str(err_no) + ' ' + ErrorCodes().get_code(str(err_no)).split(';')[0]
        description = ErrorCodes().get_code(str(err_no), ).split(';')[1]
        # description = self.error_description[arg]
        return string, description


def color_mode_info(color_mode):
    """[bits/channel, bits/pixel, total bits, nChannels]"""
    return {u.IS_CM_SENSOR_RAW16: [16, 16, 16, 1],
            u.IS_CM_SENSOR_RAW12: [12, 16, 16, 1],
            u.IS_CM_SENSOR_RAW10: [10, 16, 16, 1],
            u.IS_CM_SENSOR_RAW8: [8, 8, 8, 1],
            u.IS_CM_MONO16: [16, 16, 16, 1],
            u.IS_CM_MONO12: [12, 16, 16, 1],
            u.IS_CM_MONO10: [10, 16, 16, 1],
            u.IS_CM_MONO8: [8, 8, 8, 1],
            u.IS_CM_RGBA12_UNPACKED: [12, 36, 64, 4],
            u.IS_CM_RGB12_UNPACKED: [12, 36, 48, 3],
            u.IS_CM_RGB10_UNPACKED: [10, 30, 48, 3],
            u.IS_CM_RGB10_PACKED: [10, 30, 32, 3],
            u.IS_CM_RGBA8_PACKED: [8, 24, 32, 4],
            u.IS_CM_RGBY8_PACKED: [8, 32, 32, 4],
            u.IS_CM_RGB8_PACKED: [8, 24, 24, 3],
            u.IS_CM_BGRA12_UNPACKED: [12, 36, 64, 4],
            u.IS_CM_BGR12_UNPACKED: [12, 36, 48, 3],
            u.IS_CM_BGR10_UNPACKED: [10, 30, 48, 3],
            u.IS_CM_BGR10_PACKED: [10, 30, 32, 3],
            u.IS_CM_BGRA8_PACKED: [8, 24, 32, 4],
            u.IS_CM_BGRY8_PACKED: [8, 32, 32, 4],
            u.IS_CM_BGR8_PACKED: [8, 24, 24, 3],
            u.IS_CM_BGR565_PACKED: [5, 16, 16, 3],
            u.IS_CM_BGR5_PACKED: [5, 15, 16, 3],
            u.IS_CM_UYVY_PACKED: [8, 16, 16, 4],
            u.IS_CM_UYVY_MONO_PACKED: [8, 16, 16, 4],
            u.IS_CM_UYVY_BAYER_PACKED: [8, 16, 16, 4],
            u.IS_CM_CBYCRY_PACKED: [8, 16, 16, 4]}[color_mode]


if __name__ == '__main__':
    logger = Logger('C:/stonescanchapa/temp/sys.info')
    check(11, logger=logger)
