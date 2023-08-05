#!/usr/bin/env python

# ------------------------------------------------------------------------------
#                 PyuEye - uEye API High-Level Wrapper
#
# Copyright (c) 2017 by IDS Imaging Development Systems GmbH.
# All rights reserved.
#
# PyuEye is a lean wrapper implementation of Python function objects that
# represent uEye API functions. These bindings could be used as is.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ------------------------------------------------------------------------------

# Title: High-level wrapper for the IDS package pyueye
# Author: João Vital
# Email: joao.vital@frontwave.pt
# Company: Frontwave, S.A. - Pêro Pinheiro, Portugal
# Date: 16 - January - 2019
# Note: Only the most used functions are implemented. More functions may be implemented in future updates.
# References:
#     . pyueye_example_*.py by 	Karl Skretting

from pyueye import ueye as u
from simple_pyueye.ueye_codes import color_mode_info, uEyeException,uEyeError
from PIL import Image
import numpy as np
import win32event as we
import warnings
from time import asctime


class ImageBuffer:
    def __init__(self):
        self.ptr = u.c_mem_p()
        self.id = u.int()


class CameraObj:
    """Quick start:
            camera=Camera(camID)
            camera.open()
            camera.capture_still()
            camera.close()
            """

    def __init__(self, camID, logger=None):
        """
        Initializes the instance with a Camera ID
        :param camID: int
        """
        self.id = u.HIDS(camID)
        self.logger=logger
        self.mem = list()
        self.AOI = {'Width': int(), 'Height': int(), 'X': int(), 'Y': int()}
        self.SensorInfo = u.SENSORINFO()
        self.CameraInfo = u.CAMINFO()
        self.MultiAOIParams = u.AOI_SEQUENCE_PARAMS()
        self.ImageFormat = u.IMAGE_FORMAT_LIST()
        self.EventHandler = list()
        self.nChannels = int()
        self.bits_per_pixel = int()
        self.exposure = float()
        self.gains = [int(), int(), int(), int()]
        self.gamma = int()
        self.frame_rate = float()
        self.currContainer = None
        self.pixel_clock = int()
        self.SerialNumber = int()
        self.capture = bool()

    def check(self, command, log=None):
        """
        Check command execution. If the camera has a logger, if an error raises it will be logged.
        :param command: python command using the ueye library
        :param log: text to log if an error is raised
        :return:
        """
        nRet = command
        if nRet != 0:
            string, description = uEyeError().call(nRet)
            if self.logger is not None:
                if log is not None:
                    self.logger.log(log)

                elif self.logger.text is not None:
                    self.logger.log(self.logger.text)

                else:
                    self.logger.log('{}\n{}, {}, {}\n'.format(asctime(), nRet, string, description))

            raise uEyeException(string, description)
    
    def open(self, verbose=True):
        """
        Opens Camera instance, ready for setting parameters and capturing images
        :param verbose: bool , if True, prints a message confirming the opening of the camera.
        :return:
        """

        self.check(u.is_InitCamera(self.id, None))
        self.get_info()
        self.get_format_list()
        if verbose:
            print('Camera {} connected.'.format(self.id))

    def get_info(self):
        """
        Gathers info over the camera and sensor. Stored in CameraInfo and SensorInfo variables
        :return:
        """
        self.check(u.is_GetCameraInfo(self.id, self.CameraInfo))
        self.check(u.is_GetSensorInfo(self.id, self.SensorInfo))
        self.SerialNumber = int(self.CameraInfo.SerNo)
        self.get_multi_aoi_info()
        self.get_color_mode()
        self.get_aoi()
        """Create container with dimensions of the current camera memory to store an image"""
        self.create_container()

    def get_color_mode(self):
        """
        Gets the code of the current color mode. Sets the bits_per_pixel and nchannels accordingly to allocate memory
        and create containers for the captured images
        :return: color_mode code
        """
        color_mode = u.is_SetColorMode(self.id, u.IS_GET_COLOR_MODE)
        self.bits_per_pixel = color_mode_info(color_mode)[1]
        self.nChannels = color_mode_info(color_mode)[3]
        return color_mode

    def get_aoi(self, verbose=True):
        """
        Gets the information on the current AOI in order to allocate memory and create containers for the captured images
        :param verbose: bool , if true, prints the current AOI settings
        :return:
        """
        currrectAOI = u.IS_RECT()
        self.check(u.is_AOI(self.id, u.IS_AOI_IMAGE_GET_AOI, currrectAOI, u.sizeof(currrectAOI)))
        self.AOI['X'] = int(currrectAOI.s32X)
        self.AOI['Y'] = int(currrectAOI.s32Y)
        self.AOI['Width'] = int(currrectAOI.s32Width)
        self.AOI['Height'] = int(currrectAOI.s32Height)
        if verbose:
            print('current AOI: {}'.format(self.AOI))

    def create_container(self, current=True):
        """
        Creates a container variable for captured images
        :param current: bool , if True, uses an internal variable currContainer to allocate memory for captured images
        :return:
        """
        if current:
            self.get_aoi(verbose=False)
            self.currContainer = np.zeros((self.AOI['Height'], self.AOI['Width'], self.nChannels), dtype=np.uint8)
        else:
            return np.zeros((self.AOI['Height'], self.AOI['Width'], self.nChannels), dtype=np.uint8)

    def set_color_mode(self, color_mode):
        """
        Sets the color mode
        :param color_mode: int, in the form of ueye.IS_CM_...
        :return:
        """
        self.check(u.is_SetColorMode(self.id, color_mode))
        self.bits_per_pixel = color_mode_info(color_mode)[1]
        self.nChannels = color_mode_info(color_mode)[3]
        self.create_container()

    def alloc_mem(self, verbose=True):
        """
        Allocate memory in the camera with a pointer and an id associated
        :return:
        """
        if self.AOI['Width'] == 0:
            self.get_aoi(verbose=False)

        mem = ImageBuffer()
        # self.check(u.is_FreeImageMem(self.id, mem.ptr, mem.id))
        self.check(u.is_AllocImageMem(self.id, self.AOI['Width'], self.AOI['Height'], self.bits_per_pixel, mem.ptr, mem.id))
        self.check(u.is_SetImageMem(self.id, mem.ptr, mem.id))
        self.mem.append(mem)
        if verbose:
            print('Memory Allocated and Set. ID: {}'.format(mem.id))

    def set_aoi(self, width, height, xPos, yPos):
        """
        Sets the AOI (Area of Interest)
        :param width: int
        :param height: int
        :param xPos: int
        :param yPos: int
        :return:
        """
        AOIrect = u.IS_RECT()
        AOIrect.s32Width = u.c_int(width)
        AOIrect.s32Height = u.c_int(height)
        if xPos == 'center':
            AOIrect.s32X = u.c_int((self.SensorInfo.nMaxWidth - width) // 2)
        else:
            AOIrect.s32X = u.c_int(xPos)

        if yPos == 'center':
            AOIrect.s32Y = u.c_int((self.SensorInfo.nMaxHeight - height) // 2)
        else:
            AOIrect.s32Y = u.c_int(yPos)

        self.check(u.is_AOI(self.id, u.IS_AOI_IMAGE_SET_AOI, AOIrect, u.sizeof(AOIrect)))
        """Query the newly set AOI to confirm it's correct setting"""
        self.get_aoi()
        self.create_container()

    def set_exposure(self, value, verbose=True):
        """
        Sets a new value for the exposure time
        :param value: double
        :param verbose: bool, if True, prints the set Exposure
        :return:
        """
        value = u.c_double(value)
        self.check(u.is_Exposure(self.id, u.IS_EXPOSURE_CMD_SET_EXPOSURE, value, u.sizeof(value)))
        self.exposure = value.value
        if verbose:
            print('Exposure set to: {:.3f}'.format(value.value))

    def get_exposure(self):
        """
        Gets the current exposure time
        :return:
        """
        value = u.double()
        self.check(u.is_Exposure(self.id, u.IS_EXPOSURE_CMD_GET_EXPOSURE, value, u.sizeof(value)))
        self.exposure = value.value
        return self.exposure

    def set_fps(self, value, verbose=True):
        """
        Sets a new value for the framerate
        :param value: double
        :param verbose: bool , if True, prints the newly set value
        :return:
        """
        value = u.c_double(value)
        nvalue = u.double()
        self.check(u.is_SetFrameRate(self.id, value, nvalue))
        self.frame_rate = nvalue.value
        if verbose:
            print('Framerate set to {:.3f}'.format(nvalue.value))

    def get_fps(self):
        """
        Gets the current framerate value
        :return:
        """
        value = u.double()
        self.check(u.is_GetFramesPerSecond(self.id, value))
        self.frame_rate = value.value
        return self.frame_rate


    def set_sequence_aoi_mode(self, no_aoi):
        """
        Sets the Sequence AOI mode. self.check if your camera model supports this mode.
        :param no_aoi: int number of AOI, maximum is 4
        :return:
        """
        self.start_sequence(no_aoi)
        nMask = int()
        if no_aoi == 2:
            nMask = u.IS_AOI_SEQUENCE_INDEX_AOI_1 | u.IS_AOI_SEQUENCE_INDEX_AOI_2
        elif no_aoi == 3:
            nMask = u.IS_AOI_SEQUENCE_INDEX_AOI_1 | u.IS_AOI_SEQUENCE_INDEX_AOI_2 | u.IS_AOI_SEQUENCE_INDEX_AOI_3
        elif no_aoi == 4:
            nMask = u.IS_AOI_SEQUENCE_INDEX_AOI_1 | u.IS_AOI_SEQUENCE_INDEX_AOI_2 | u.IS_AOI_SEQUENCE_INDEX_AOI_3 | u.IS_AOI_SEQUENCE_INDEX_AOI_4
        self.check(u.is_AOI(self.id, u.IS_AOI_SEQUENCE_SET_ENABLE, u.c_int(nMask), u.sizeof(u.c_int(nMask))))

    def set_sequence_aoi_params(self, aoi_index, exposure, gain, xPos, yPos, detatch=True, readout=1):
        """
        Sets the parameters for a Sequence AOI
        :param aoi_index: int , in the form of ex: u.IS_AOI_SEQUENCE_INDEX_AOI_2
        :param exposure: double
        :param gain: int
        :param xPos: int
        :param yPos: int
        :param detatch: bool , if True, settings from the main AOI are not automatically copied to the other Sequence AOIs
        :param readout: int , determines how many times the AOI are read. defaults to 1
        :return:
        """
        p = u.AOI_SEQUENCE_PARAMS()
        p.s32AOIIndex = u.c_int(aoi_index)
        p.dblExposure = u.c_double(exposure)
        p.s32Gain = u.c_int(gain)
        p.s32DetatchImageParameters = u.c_int(int(detatch))
        p.s32NumberOfCycleRepetitions = u.c_int(readout)
        p.s32X = u.c_int(xPos)
        p.s32Y = u.c_int(yPos)
        self.check(u.is_AOI(self.id, u.IS_AOI_SEQUENCE_SET_PARAMS, p, u.sizeof(p)))

    def set_pixelclock(self, value, verbose=True):
        """
        Sets a new Pixel Clock value
        :param value: int
        :param verbose: bool , if True, prints the set value
        :return:
        """
        value = u.c_uint(value)
        curr_value = u.c_uint()
        self.check(u.is_PixelClock(self.id, u.IS_PIXELCLOCK_CMD_SET, value, u.sizeof(value)))
        self.check(u.is_PixelClock(self.id, u.IS_PIXELCLOCK_CMD_GET, curr_value, u.sizeof(curr_value)))
        self.pixel_clock = curr_value.value
        if verbose:
            print('PixelClock set to: {}'.format(curr_value))

    def set_hardware_gains(self, values, verbose=True):
        """
        Sets values for the hardware gains
        :param values: list of int, in the form of [MASTER, RED_GAIN, GREEN_GAIN, BLUE_GAIN].
                If you do not wish to change one of the entries, set to ueye.IS_IGNORE_PARAMETER or -1
        :param verbose: bool, if True, print the set gains
        :return:
        """
        master = u.c_int(values[0])
        r_gain = u.c_int(values[1])
        g_gain = u.c_int(values[2])
        b_gain = u.c_int(values[3])
        self.check(u.is_SetHardwareGain(self.id, master, r_gain, g_gain, b_gain))
        self.gains = [master.value, r_gain.value, g_gain.value, b_gain.value]
        if verbose:
            print('Set gains: {}'.format(values))

    def set_gamma(self, value, verbose=True):
        """
        Sets a new gamma value
        :param value: int
        :param verbose: bool , if True, prints the set value
        :return:
        """
        value = u.c_int(int(value))
        self.check(u.is_Gamma(self.id, u.IS_GAMMA_CMD_SET, value, u.sizeof(value)))
        self.gamma = value.value
        if verbose:
            print('Gamma set to: {}'.format(value))

    def install_event(self, event):
        """
        Installs an event and appends it to the EventHandler variable
        :param event: int, code of the event, in the form of ueye.IS_EVENT...
        :return:
        """
        hEv_py = we.CreateEvent(None, 0, 0, None)
        hEv = u.c_void_p(int(hEv_py))
        self.check(u.is_InitEvent(self.id, hEv, event))
        self.check(u.is_EnableEvent(self.id, event))
        self.EventHandler.append(hEv_py)

    def set_trigger_mode(self, trigger_mode, verbose=True):
        """
        Sets a trigger mode
        :param trigger_mode: int, trigger mode code, in the form of ueye.IS_SET_TRIGGER...
        :param verbose: bool , if True, prints a message confirming the success of the operation
        :return:
        """
        self.check(u.is_SetExternalTrigger(self.id, trigger_mode))
        if verbose:
            print('Set Trigger Mode')

    def set_prescaler(self, value, verbose=True):
        """
        Sets a value for the prescaler. The camera will be triggered every 'value' signals.
        i.e. The camera skips 'value' signals
        :param value: int, prescaler value to set
        :param verbose: bool, if True, prints the set value
        :return:
        """
        value = u.c_uint(value)
        self.check(u.is_Trigger(self.id, u.IS_TRIGGER_CMD_SET_FRAME_PRESCALER, value, u.sizeof(value)))
        if verbose:
            print('Prescaler set to: {}'.format(value.value))

    def close(self, verbose=True):
        """
        Closes the camera
        :param verbose: bool , if True, prints a message confirming the success of the operation.
        :return:
        """
        for mem in self.mem:
            self.check(u.is_UnlockSeqBuf(self.id, mem.id, mem.ptr))
            self.check(u.is_FreeImageMem(self.id, mem.ptr, mem.id))
        self.check(u.is_ExitCamera(self.id))
        if verbose:
            print('Camera {} disconnected'.format(self.id))

    def get_format_list(self):
        """
        Retrieves the possible predefined image formats
        :return:
        """
        count = u.c_uint()
        self.check(u.is_ImageFormat(self.id, u.IMGFRMT_CMD_GET_NUM_ENTRIES, count, u.sizeof(count)))
        pformatList = u.IMAGE_FORMAT_LIST(FormatInfo=(u.IMAGE_FORMAT_INFO * count))
        pformatList.nNumListElements = count
        pformatList.nSizeOfListEntry = u.sizeof(u.IMAGE_FORMAT_INFO)
        self.check(u.is_ImageFormat(self.id, u.IMGFRMT_CMD_GET_LIST, pformatList, u.sizeof(pformatList)))
        self.ImageFormat = pformatList

    def set_image_format(self, format_id):
        """
        Sets a predefined image format. self.check the available formats in the uEye Cockpit
        :param format_id: int, format coe number
        :return:
        """
        formatInfo = self.ImageFormat.FormatInfo[format_id]
        self.check(u.is_ImageFormat(self.id, u.IMGFRMT_CMD_SET_FORMAT, formatInfo.nFormatID, u.sizeof(formatInfo.nFormatID)))
        self.get_aoi()

    def get_multi_aoi_info(self):
        """
        Initializes the structures needed for multi AOI.
        :return:
        """
        m_nMaxNumberMultiAOIs = u.uint()
        self.check(u.is_AOI(self.id, u.IS_AOI_MULTI_GET_AOI | u.IS_AOI_MULTI_MODE_GET_MAX_NUMBER, m_nMaxNumberMultiAOIs,
                       u.sizeof(m_nMaxNumberMultiAOIs)))
        rMinSizeAOI = u.IS_SIZE_2D()
        self.check(u.is_AOI(self.id, u.IS_AOI_MULTI_GET_AOI | u.IS_AOI_MULTI_MODE_GET_MINIMUM_SIZE, rMinSizeAOI,
                       u.sizeof(rMinSizeAOI)))
        if m_nMaxNumberMultiAOIs > 1:
            m_psMultiAOIs = u.IS_MULTI_AOI_CONTAINER(pMultiAOIList=(u.IS_MULTI_AOI_DESCRIPTOR * m_nMaxNumberMultiAOIs))
            m_psMultiAOIs.nNumberOfAOIs = m_nMaxNumberMultiAOIs
            self.MultiAOIParams = m_psMultiAOIs

    def set_multi_aoi_param(self, aoi_index, xPos, yPos, width, height):
        """
        Set the parameters of a specified AOI. Keep in mind that the camera concatenates all AOIs in the MultiAOIList,
        hence the positions and sizes must be so that the set forms a rectangle.
        See documentation for further clarification.
        :param aoi_index: int , number of the AOI to set the parameters for
        :param xPos: int
        :param yPos: int
        :param width: int
        :param height: int
        :return:
        """
        self.MultiAOIParams.pMultiAOIList[aoi_index].nPosX = u.c_uint(xPos)
        self.MultiAOIParams.pMultiAOIList[aoi_index].nPosY = u.c_uint(yPos)
        self.MultiAOIParams.pMultiAOIList[aoi_index].nWidth = u.c_uint(width)
        self.MultiAOIParams.pMultiAOIList[aoi_index].nHeight = u.c_uint(height)
        self.MultiAOIParams.pMultiAOIList[aoi_index].nStatus = u.c_uint(u.IS_AOI_MULTI_STATUS_SETBYUSER)

    def start_multi_aoi(self):
        """
        Verifies the MultiAOI settings and sets them if everything is OK.
        :return:
        """
        self.check(u.is_AOI(self.id, u.IS_AOI_MULTI_SET_AOI | u.IS_AOI_MULTI_MODE_ONLY_VERIFY_AOIS, self.MultiAOIParams,
                       u.sizeof(u.IS_MULTI_AOI_CONTAINER()) + u.sizeof(
                           u.IS_MULTI_AOI_DESCRIPTOR()) * self.MultiAOIParams.nNumberOfAOIs))
        self.check(u.is_AOI(self.id, u.IS_AOI_MULTI_SET_AOI, self.MultiAOIParams, u.sizeof(self.MultiAOIParams)))
        self.create_container()

    def start_sequence(self, no_buffs):
        """
        Starts a sequence of 'no_buffs' buffers. This is important to ensure all frames are captured even if there is a
        delay of more than the capturing time between two frames.
        :param no_buffs: int, number of buffers to allocate
        :return:
        """
        for i in range(no_buffs):
            mem = ImageBuffer()
            self.check(u.is_AllocImageMem(self.id, self.AOI['Width'], self.AOI['Height'], self.bits_per_pixel, mem.ptr,
                                     mem.id))
            self.mem.append(mem)

        for mem in self.mem:
            self.check(u.is_AddToSequence(self.id, mem.ptr, mem.id))

        self.check(u.is_InitImageQueue(self.id, 0))

    def set_trigger_debounce(self, mode='auto', delay=None, verbose=True):
        """
        :param mode: str, defaults to auto, can be ['auto', 'rising', 'falling', 'both']
        :param delay: int, sets the time the signal has to be on to be considered
        :param verbose: bool, whether or not to display a message confirming the operation
        :return:
        """
        if mode == 'auto':
            self.check(u.is_TriggerDebounce(self.id, u.TRIGGER_DEBOUNCE_CMD_SET_MODE,
                                       u.c_uint(u.TRIGGER_DEBOUNCE_MODE_AUTOMATIC),
                                       u.sizeof(u.c_uint(u.TRIGGER_DEBOUNCE_MODE_AUTOMATIC))))

        elif mode == 'rising':
            self.check(u.is_TriggerDebounce(self.id, u.TRIGGER_DEBOUNCE_CMD_SET_MODE, u.TRIGGER_DEBOUNCE_MODE_RISING_EDGE,
                                       u.sizeof(u.TRIGGER_DEBOUNCE_MODE_RISING_EDGE)))

        elif mode == 'falling':
            self.check(u.is_TriggerDebounce(self.id, u.TRIGGER_DEBOUNCE_CMD_SET_MODE, u.TRIGGER_DEBOUNCE_MODE_FALLING_EDGE,
                                       u.sizeof(u.TRIGGER_DEBOUNCE_MODE_FALLING_EDGE)))

        elif mode == 'both':
            self.check(u.is_TriggerDebounce(self.id, u.TRIGGER_DEBOUNCE_CMD_SET_MODE, u.TRIGGER_DEBOUNCE_MODE_BOTH_EDGES,
                                       u.sizeof(u.TRIGGER_DEBOUNCE_MODE_BOTH_EDGES)))

        else:
            self.check(u.is_TriggerDebounce(self.id, u.TRIGGER_DEBOUNCE_CMD_SET_MODE, u.TRIGGER_DEBOUNCE_MODE_NONE,
                                       u.sizeof(u.TRIGGER_DEBOUNCE_MODE_NONE)))
        if verbose:
            print('Trigger debounce mode set to: {}'.format(mode))

        if delay is not None:
            delay = u.c_uint(int(delay))
            self.check(u.is_TriggerDebounce(self.id, u.TRIGGER_DEBOUNCE_CMD_SET_DELAY_TIME, delay, u.sizeof(delay)))
            if verbose:
                print('Trigger debounce delay set successfully to: {}'.format(delay))

    def stop_live_video(self, verbose=False):
        self.check(u.is_StopLiveVideo(self.id, u.IS_DONT_WAIT))
        if verbose:
            print('Live video from camera {} stopped...'.format(self.id))

    def execute(self,command):
        """
        Execute a command and wrap it with this object's logger
        :param command:
        :return:
        """
        self.check(command)

    def capture_still(self, save=False, filename='sample.png'):
        """
        Captures a still picture
        :param save: bool , if True, image is saved to a file, if not, a numpy array will be returned containing the image
        :param filename: string , with the path to the file where the captured image will be stored
        :return:
        """
        if self.mem.__len__() == 0:
            warnings.warn('Warning: Memory not allocated! Allocating memory to default AOI...')
            self.alloc_mem()

        self.check(u.is_FreezeVideo(self.id, u.IS_WAIT))
        mem = ImageBuffer()
        self.check(u.is_GetActiveImageMem(self.id, mem.ptr, mem.id))
        self.check(u.is_CopyImageMem(self.id, mem.ptr, mem.id, self.currContainer.ctypes.data))
        if save:
            im = Image.fromarray(self.currContainer)
            im.save(filename)
        return self.currContainer

    def continuous_capture(self):
        """
        Run this preferably inside a Thread.
        :return:
        """
        if self.mem.__len__() == 0:
            warnings.warn('Warning: Memory not allocated! Allocating memory to default AOI...')
            self.alloc_mem()

        if self.EventHandler.__len__() == 0:
            warnings.warn('Warning: Frame Event not installed! Installing...')
            self.install_event(u.IS_FRAME)

        self.capture = True
        self.check(u.is_CaptureVideo(self.id, u.IS_WAIT))
        while self.capture:
            mem = ImageBuffer()
            we.WaitForSingleObject(self.EventHandler[0], we.INFINITE)
            self.check(u.is_GetActiveImageMem(self.id, mem.ptr, mem.id))
            self.check(u.is_CopyImageMem(self.id, mem.ptr, mem.id, self.currContainer.ctypes.data))
            self.check(u.is_UnlockSeqBuf(self.id, mem.id, mem.ptr))

            """Place further processing code here
                Image is placed in self currContainer"""

        self.stop_live_video()


if __name__ == '__main__':
    from simple_pyueye.ueye_codes import Logger
    logger = Logger('C:/stonescanchapa/temp/sys.info')
    cam = CameraObj(0, logger=logger)
    cam.execute(u.is_InitCamera(cam.id,None))
    # cam.open()
    # cam.capture_still(save=True, filename='img.png')
    cam.close()
