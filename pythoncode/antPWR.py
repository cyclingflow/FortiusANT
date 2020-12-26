#-------------------------------------------------------------------------------
# Version info
#-------------------------------------------------------------------------------
__version__ = "2020-06-11"
# 2020-06-11    First version, based upon antHRM.py
#-------------------------------------------------------------------------------
import time
import antDongle         as ant

def Initialize():
    global EventCount, AccumulatedPower, LastPower
    EventCount          = 0
    AccumulatedPower    = 0
    LastPower           = 0

def BroadcastMessage (CurrentPower, Cadence):
    global EventCount, AccumulatedPower, LastPower

    #-------------------------------------------------------------------------
    # Update eventcount and accumulated power if needed:
    # event count is only increased if currentpower>0,
    # and more time if currentpower = 0
    #-------------------------------------------------------------------------

    if LastPower>0 or CurrentPower>0:
        EventCount = (EventCount+1)%256
        AccumulatedPower = (AccumulatedPower+CurrentPower)%65536
        LastPower = CurrentPower

    if   EventCount % 120 == 0:           # Transmit page 0x50 = 80
        info = ant.msgPage80_ManufacturerInfo(ant.channel_PWR, 0xff, 0xff, \
            ant.HWrevision_PWR, ant.Manufacturer_garmin, ant.ModelNumber_PWR)

    elif EventCount % 131 == 0:           # Transmit page 0x51 = 81
    #elif EventCount % 121 == 0:           # Transmit page 0x51 = 81
        info = ant.msgPage81_ProductInformation(ant.channel_PWR, 0xff, \
            ant.SWrevisionSupp_PWR, ant.SWrevisionMain_PWR, ant.SerialNumber_PWR)

    elif EventCount %  60 == 0:           # Transmit page 0x52 = 82
        info = ant.msgPage82_BatteryStatus(ant.channel_PWR)
    
    else:
        info= ant.msgPage16_PowerOnly (ant.channel_PWR, EventCount, Cadence, AccumulatedPower, CurrentPower)

    pwrdata = ant.ComposeMessage (ant.msgID_BroadcastData, info)

    #-------------------------------------------------------------------------
    # Return message to be sent
    #-------------------------------------------------------------------------
    return pwrdata

#-------------------------------------------------------------------------------
# Main program for module test
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    Initialize()
    pwrdata = BroadcastMessage (456.7, 123)
    print (pwrdata)