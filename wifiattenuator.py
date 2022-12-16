import usb.core
import usb.util
import globalfunctions as gf, globalparams as gp

class WiFi_Attenuator():
    
#-----------------------CLASS-LEVEL VARIABLES-----------------------#
    
    serial_number = ""
    
    model_number = ""
    
    firmware = ""
    
    dev = usb.core.find(idVendor=gp.VENDOR_ID, idProduct=gp.PRODUCT_ID) # CLASS-LEVEL PARAM OF ATTENUATOR
    
    def __init__(self):
        
        #-----------CATCH ERROR IF DEVICE CANNOT BE FOUND-------------#
        
        if self.dev is None:
            raise ValueError('DEVICE NOT FOUND')


        #-----------INITIALISE WIFI ATTENUATOR DEVICE CONFIGURATION-------------#
        
        for configuration in self.dev:
            for interface in configuration:
                ifnum = interface.bInterfaceNumber
                if not self.dev.is_kernel_driver_active(ifnum):
                    continue
                self.dev.detach_kernel_driver(ifnum)

        self.dev.set_configuration()
        
        
        #-----------GET DEVICE DETAILS-------------#
        
        self.get_serial_number()
        self.get_model_number()
        self.get_firmware()
        
        gf.console_log("SERIAL NUMBER IS: {0}".format(self.serial_number))
        gf.console_log("MODEL NUMBER IS: {0}".format(self.model_number))
        gf.console_log("FIRMWARE IS: {0}".format(self.firmware))
        
        self.init_all_attenuation()
        

#-----------------------CLASS METHODS FOR I/O-----------------------#

    def write_to_attenuator(self, scpi):
        self.dev.write(1, scpi)
        return
    
    
    def read_from_attenuator(self):
        rtn_byte_array = self.dev.read(0x81,64)
        rtn_string = ""
        it = 1
        
        while (rtn_byte_array[it] < 255 and rtn_byte_array[it] > 0):
            rtn_string += chr(rtn_byte_array[it])
            it += 1
            
        return rtn_string

#-----------------------CLASS METHODS TO INITIALISE DEVICE-----------------------#
    
    def get_serial_number(self):
        self.write_to_attenuator(gp.GET_SN)
        self.serial_number = self.read_from_attenuator()
        return
    
    
    def get_model_number(self):
        self.write_to_attenuator(gp.GET_MN)
        self.model_number = self.read_from_attenuator()
        return
    
    
    def get_firmware(self):
        self.write_to_attenuator(gp.GET_FW)
        self.firmware = self.read_from_attenuator()
        return
    
    
    def init_all_attenuation(self):
        self.write_to_attenuator(gp.INIT_MAX_ATT_CHAN_FOUR)
        cfour_to_max = self.read_from_attenuator()
        self.write_to_attenuator(gp.INIT_ATT_ALL_CHAN)
        allch_to_zero = self.read_from_attenuator()
        self.write_to_attenuator(gp.GET_ATT)
        rtn = self.read_from_attenuator()
        
        if cfour_to_max != "1" or allch_to_zero != "1":
            raise Exception("ATTENUATOR INIT UNSUCCESSFUL")
        
        gf.console_log("ATTENUATOR INIT SUCCESFUL")
        gf.console_log("ATTENUATOR VALUES: {0}".format(rtn))
        return
    
    
    def get_attenuation(self):
        self.write_to_attenuator(gp.GET_ATT)
        attenuation = self.read_from_attenuator()
        return attenuation
    
    
    def set_all_channels_attenuation(self, attn_val):
        if attn_val < 10:
            attn_val = "0" + str(attn_val)
        self.write_to_attenuator(gp.SET_ALL_ATT.format(attn_val))
        rtn = self.read_from_attenuator()
        self.write_to_attenuator(gp.GET_ATT)
        rtn = self.read_from_attenuator()
        gf.console_log("EDITED ATTENUATOR VALUES: {0}".format(rtn))
        return
    
    