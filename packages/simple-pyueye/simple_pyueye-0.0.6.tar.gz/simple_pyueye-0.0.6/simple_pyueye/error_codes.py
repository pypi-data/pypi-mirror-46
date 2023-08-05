class ErrorCodes:
    def __init__(self):
        codes = dict()
        codes['-1'] = 'IS_NO_SUCCESS;General error message'
        codes['0'] = 'IS_SUCCESS;Function executed successfully'
        codes[
            '1'] = 'IS_INVALID_CAMERA_HANDLE;Invalid camera handle Most of the uEye SDK functions expect the camera handle as the first parameter.'
        codes[
            '2'] = 'IS_IO_REQUEST_FAILED;An IO request from the uEye driver failed. Possibly the versions of the ueye_api.dll (API) and the driver file (ueye_usb.sys or ueye_eth.sys) do not match.'
        codes[
            '3'] = 'IS_CANT_OPEN_DEVICE;An attempt to initialize or select the camera failed (no camera connected or initialization error).'
        codes['11'] = 'IS_CANT_OPEN_REGISTRY;Error opening a Windows registry key'
        codes['12'] = 'IS_CANT_READ_REGISTRY;Error reading settings from the Windows registry'
        codes['15'] = 'IS_NO_IMAGE_MEM_ALLOCATED;The driver could not allocate memory.'
        codes['16'] = 'IS_CANT_CLEANUP_MEMORY;The driver could not release the allocated memory.'
        codes[
            '17'] = 'IS_CANT_COMMUNICATE_WITH_DRIVER;Communication with the driver failed because no driver has been loaded.'
        codes['18'] = 'IS_FUNCTION_NOT_SUPPORTED_YET;The function is not supported yet.'
        codes['30'] = 'IS_INVALID_IMAGE_SIZE;Invalid image size'
        codes[
            '32'] = 'IS_INVALID_CAPTURE_MODE;The function can not be executed in the current camera operating mode (free run, trigger or standby).'
        codes['49'] = 'IS_INVALID_MEMORY_POINTER;Invalid pointer or invalid memory ID'
        codes['50'] = 'IS_FILE_WRITE_OPEN_ERROR;File cannot be opened for writing or reading.'
        codes['51'] = 'IS_FILE_READ_OPEN_ERROR;The file cannot be opened.'
        codes['52'] = 'IS_FILE_READ_INVALID_BMP_ID;The specified file is not a valid bitmap file.'
        codes['53'] = 'IS_FILE_READ_INVALID_BMP_SIZE;The bitmap size is not correct (bitmap too large).'
        codes[
            '108'] = 'IS_NO_ACTIVE_IMG_MEM;No active image memory available. You must set the memory to active using the is_SetImageMem() function or create a sequence using the is_AddToSequence() function.'
        codes['112'] = 'IS_SEQUENCE_LIST_EMPTY;The sequence list is empty and cannot be deleted.'
        codes[
            '113'] = 'IS_CANT_ADD_TO_SEQUENCE;The image memory is already included in the sequence and cannot be added again.'
        codes[
            '117'] = 'IS_SEQUENCE_BUF_ALREADY_LOCKED;The memory could not be locked. The pointer to the buffer is invalid.'
        codes[
            '118'] = 'IS_INVALID_DEVICE_ID;The device ID is invalid. Valid IDs start from 1 for USB cameras, and from 1001 for GigE cameras.'
        codes['119'] = 'IS_INVALID_BOARD_ID;The board ID is invalid. Valid IDs range from 1 through 255.'
        codes['120'] = 'IS_ALL_DEVICES_BUSY;All cameras are in use.'
        codes[
            '122'] = 'IS_TIMED_OUT;A timeout occurred. An image capturing process could not be terminated within the allowable period.'
        codes['123'] = 'IS_NULL_POINTER;Invalid array'
        codes[
            '125'] = 'IS_INVALID_PARAMETER;One of the submitted parameters is outside the valid range or is not supported for this sensor or is not available in this mode.'
        codes['127'] = 'IS_OUT_OF_MEMORY;No memory could be allocated.'
        codes['129'] = 'IS_ACCESS_VIOLATION;An internal error has occurred.'
        codes[
            '139'] = 'IS_NO_USB20;The camera is connected to a port which does not support the USB 2.0 high-speed standard. Cameras without a memory board cannot be operated on a USB 1.1 port.'
        codes['140'] = 'IS_CAPTURE_RUNNING;A capturing operation is in progress and must be terminated first.'
        codes[
            '145'] = 'IS_IMAGE_NOT_PRESENT;The requested image is not available in the camera memory or is no longer valid.'
        codes[
            '148'] = 'IS_TRIGGER_ACTIVATED;The function cannot be used because the camera is waiting for a trigger signal.'
        codes['151'] = 'IS_CRC_ERROR;A CRC error-correction problem occurred while reading the settings.'
        codes['152'] = 'IS_NOT_YET_RELEASED;This function has not been enabled yet in this version.'
        codes['153'] = 'IS_NOT_CALIBRATED;The camera does not contain any calibration data.'
        codes['154'] = 'IS_WAITING_FOR_KERNEL;The system is waiting for the kernel driver to respond.'
        codes['155'] = 'IS_NOT_SUPPORTED;The camera model used here does not support this function or setting.'
        codes['156'] = 'IS_TRIGGER_NOT_ACTIVATED;The function is not possible as trigger is disabled.'
        codes[
            '157'] = 'IS_OPERATION_ABORTED;The dialog was canceled without a selection so that no file could be saved.'
        codes['158'] = 'IS_BAD_STRUCTURE_SIZE;An internal structure has an incorrect size.'
        codes[
            '159'] = 'IS_INVALID_BUFFER_SIZE;The image memory has an inappropriate size to store the image in the desired format.'
        codes[
            '160'] = 'IS_INVALID_PIXEL_CLOCK;This setting is not available for the currently set pixel clock frequency.'
        codes['161'] = 'IS_INVALID_EXPOSURE_TIME;This setting is not available for the currently set exposure time.'
        codes[
            '162'] = 'IS_AUTO_EXPOSURE_RUNNING;This setting cannot be changed while automatic exposure time control is enabled.'
        codes['163'] = 'IS_CANNOT_CREATE_BB_SURF;The BackBuffer surface cannot be created.'
        codes['164'] = 'IS_CANNOT_CREATE_BB_MIX;The BackBuffer mix surface cannot be created.'
        codes['165'] = 'IS_BB_OVLMEM_NULL;The BackBuffer overlay memory cannot be locked.'
        codes['166'] = 'IS_CANNOT_CREATE_BB_OVL;The BackBuffer overlay memory cannot be created.'
        codes['167'] = 'IS_NOT_SUPP_IN_OVL_SURF_MODE;Not supported in BackBuffer Overlay mode.'
        codes['168'] = 'IS_INVALID_SURFACE;Back buffer surface invalid.'
        codes['169'] = 'IS_SURFACE_LOST;Back buffer surface not found.'
        codes['170'] = 'IS_RELEASE_BB_OVL_DC;Error releasing the overlay device context.'
        codes['171'] = 'IS_BB_TIMER_NOT_CREATED;The back buffer timer could not be created.'
        codes['172'] = 'IS_BB_OVL_NOT_EN;The back buffer overlay was not enabled.'
        codes['173'] = 'IS_ONLY_IN_BB_MODE;Only possible in BackBuffer mode.'
        codes['174'] = 'IS_INVALID_COLOR_FORMAT;Invalid color format'
        codes[
            '175'] = 'IS_INVALID_WB_BINNING_MODE;Mono binning/mono sub-sampling do not support automatic white balance.'
        codes['176'] = 'IS_INVALID_I2C_DEVICE_ADDRESS;Invalid I2C device address'
        codes['177'] = 'IS_COULD_NOT_CONVERT;The current image could not be processed.'
        codes[
            '178'] = 'IS_TRANSFER_ERROR;Transfer error. Frequent transfer errors can mostly be avoided by reducing the pixel rate.'
        codes['179'] = 'IS_PARAMETER_SET_NOT_PRESENT;Parameter set is not present.'
        codes[
            '180'] = 'IS_INVALID_CAMERA_TYPE;The camera type defined in the .ini file does not match the current camera model.'
        codes['181'] = 'IS_INVALID_HOST_IP_HIBYTE;Invalid HIBYTE of host address.'
        codes['182'] = 'IS_CM_NOT_SUPP_IN_CURR_DISPLAYMODE;The color mode is not supported in the current display mode.'
        codes['183'] = 'IS_NO_IR_FILTER;No IR filter available'
        codes[
            '184'] = "IS_STARTER_FW_UPLOAD_NEEDED;The camera's starter firmware is not compatible with the driver and needs to be updated."
        codes['185'] = 'IS_DR_LIBRARY_NOT_FOUND;The DirectRenderer library could not be found.'
        codes['186'] = 'IS_DR_DEVICE_OUT_OF_MEMORY;Not enough graphics memory available.'
        codes['187'] = 'IS_DR_CANNOT_CREATE_SURFACE;The image surface or overlay surface could not be created.'
        codes['188'] = 'IS_DR_CANNOT_CREATE_VERTEX_BUFFER;The vertex buffer could not be created.'
        codes['189'] = 'IS_DR_CANNOT_CREATE_TEXTURE;The texture could not be created.'
        codes['190'] = 'IS_DR_CANNOT_LOCK_OVERLAY_SURFACE;The overlay surface could not be locked.'
        codes['191'] = 'IS_DR_CANNOT_UNLOCK_OVERLAY_SURFACE;The overlay surface could not be unlocked.'
        codes['192'] = 'IS_DR_CANNOT_GET_OVERLAY_DC;Could not get the device context handle for the overlay.'
        codes['193'] = 'IS_DR_CANNOT_RELEASE_OVERLAY_DC;Could not release the device context handle for the overlay.'
        codes['194'] = 'IS_DR_DEVICE_CAPS_INSUFFICIENT;Function is not supported by the graphics hardware.'
        codes['195'] = 'IS_INCOMPATIBLE_SETTING;Because of other incompatible settings the function is not possible.'
        codes['196'] = 'IS_DR_NOT_ALLOWED_WHILE_DC_IS_ACTIVE;A device context handle is still open in the application.'
        codes['197'] = 'IS_DEVICE_ALREADY_PAIRED;The device is already paired.'
        codes['198'] = 'IS_SUBNETMASK_MISMATCH;The subnet mask of the camera and PC network card are different.'
        codes['199'] = 'IS_SUBNET_MISMATCH;The subnet of the camera and PC network card are different.'
        codes['200'] = 'IS_INVALID_IP_CONFIGURATION;The configuration of the IP address is invalid.'
        codes['201'] = 'IS_DEVICE_NOT_COMPATIBLE;The device is not compatible to the drivers.'
        codes[
            '202'] = 'IS_NETWORK_FRAME_SIZE_INCOMPATIBLE;The settings for the image size of the camera are not compatible to the PC network card.'
        codes['203'] = 'IS_NETWORK_CONFIGURATION_INVALID;The configuration of the network card is invalid.'
        codes['204'] = 'IS_ERROR_CPU_IDLE_STATES_CONFIGURATION;The configuration of the CPU idle has failed.'
        codes['205'] = 'IS_DEVICE_BUSY;The camera is busy and cannot transfer the requested image.'
        codes['206'] = 'IS_SENSOR_INITIALIZATION_FAILED;The initialization of the sensor failed.'
        codes['207'] = 'IS_IMAGE_BUFFER_NOT_DWORD_ALIGNED;The image buffer is not DWORD aligned.'
        codes['208'] = 'IS_SEQ_BUFFER_IS_LOCKED;The image memory is locked.'
        codes['209'] = 'IS_FILE_PATH_DOES_NOT_EXIST;The file path does not exist.'
        codes['210'] = 'IS_INVALID_WINDOW_HANDLE;Invalid Window handle'
        self.codes = codes

    def get_code(self, code):
        return self.codes[code] if code in self.codes.keys() else self.codes['-1']
