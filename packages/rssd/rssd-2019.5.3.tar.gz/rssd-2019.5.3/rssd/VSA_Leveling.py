import re

def Optimise_FSx_Level(self,lvlTable):
    ####################################################################
    """ Algorithm designed by Darren Tipton & Florian Ramien"""
    """ Optimise level for Mixer Input => Optimal EVM """
    """ Optimises for signals using IF gain as well as attenuation """    
    ####################################################################
    #Variables used:
    #   maxmix:             maximum mixer/PA input level; RFAtt will be used to keep this
    #   gain:               nominal gain of amplifiers, limits maximum settable RefLevel
    #   rfatt:              RFAttenuator setting
    #   RfattStepSize:      Step size of RF attenuator
    #   reflev:             Reference level setting
    #   RefLevelStepSize:   step size of ref level setting
    #   level:              signal power from measurement
    RfattStepSize = 5
    RefLevelStepSize = 1
    isFSV3k = 0

    # initial measurement of power to get an estimate for the power
    self.Set_Channel('IQ','Level')
    markerlevel = sum(map(float, self.query("INIT:IMM;*WAI;:CALC:MARK:MAX;Y?;MIN;Y?").split(";")))/2
    level = round(markerlevel)
    try:
        rfatt = lvlTable[level][0]
    except:
        rfatt = None

    freq = self.Get_Freq()

    # if dictionary has value for current level, use it, else below routine
    # instrument dependent settings
    # define maximum mixer level, before we see significant compression
    # this includes measured gain, as the gain variable only takes care about the nominal gain
    if isFSV3k:                                 #FSV3k has 2 amplifier stages 1: 30 dB nominal, 2: 15 dB nominal
        if level >= -10:
            self.Set_Preamp(0)
            gain = 0
            maxmix = 0 if freq < 7.5e9 else -10
        elif level >= -31:
            self.query("INP:GAIN:VAL 15;STAT ON;*OPC?")
            gain = 15
            maxmix = -20 if freq < 7.5e9 else -25
        else:
            self.query("INP:GAIN:VAL 30;STAT ON;*OPC?")
            gain = 30
            maxmix = -33 if freq < 7.5e9 else -33
    else:        # valid for FSW
        if level >= -10:
            self.Set_Preamp(0)
            gain = 0
            maxmix = 0 if freq < 8e9 else -10 
        else:
            self.Set_Preamp(1)
            gain = 30
            maxmix = -30 if freq < 8e9 else -40

    if rfatt == None:
        rfatt = level - maxmix                  # Calc atten for optimal mixer level - we need a start point for iterating

    if rfatt < 0:                               # we will always do this, even in table mode
        rfatt = 0
    rfatt = round(rfatt / RfattStepSize) * RfattStepSize 
 
    self.Set_AttnMech(rfatt)                    # Set initial attenuation 
    reflev = maxmix + rfatt                     # Set initial ref level
    self.Set_RefLevel(reflev)
    ifovl = self.Get_IFOvld()                   # Check if there is IF Overload based on initial settings

    """ Iterating / Optimising for attenuation - Best SNR """
    while ifovl != "0":                         # If there is an IF OLV increase attenuation
        rfatt = rfatt + RfattStepSize
        self.Set_AttnMech(rfatt)
        reflev = maxmix + rfatt                 # new ref level accounting for new attenuation 
        self.Set_RefLvl(reflev)
        ifovl = self.Get_IFOvld()               # Check if there is IF Overload on new settings

    try:
        reflev = lvlTable[level][1]
    except:
        reflev = None
    if reflev == None:
        # perform only if dictionary has no entry for current level
        # we know that reflevmax does not produce an overload!
        reflevmax = 0 + rfatt - gain            # assuming 0 dBm max mixer level
        reflevmin = 0 + rfatt - gain - 20       # assuming 20 dB IF gain
 
        """ Iterating / Optimising for reference level """
        while abs(reflevmax-reflevmin) > RefLevelStepSize:
            """ If there isn't an IF OVL bring the ref level down """
            reflev = reflevmax - (reflevmax-reflevmin)/2
            self.Set_RefLevel(reflev)

            ifovl = self.Get_IFOvld()           # Check if there is IF Overload on new settings

            # Now change the max and min depending on whether we have an OVLD
            # OVLD: max stays (now OVLD), min is reflev (OVLD)
            if ifovl:
                reflevmin = reflev
            else:
                reflevmax = reflev
                
        #after loop (less than 1 dB difference), assign reflevmax (no OVLD) to reflev and use it
        reflev = reflevmin
        reflev = round(reflev / RefLevelStepSize)*RefLevelStepSize

    ifovl = self.Get_IFOvld()                   # Final check for IF Overload before we take the measurement

    """ If IF OVL occurs back off ref level by 1dB """
    if ifovl != "0":
        reflev = reflev + RefLevelStepSize
        self.Set_RefLvl(reflev)


    # RfAttSet[level]= rfatt
    # RefLevelSet[level]= reflev
    # return RfAttSet, RefLevelSet
    lvlTable[level] = [rfatt,reflev]
    return lvlTable

def ReadLevellingTables(freq):
    import os
    import json
    LvlTable = {}

    #TODO: Round frequency to 100 MHz - experimental; Verify frequency raster
    filenameLvlTables = "LevelTables_5GNR_" + str(round(freq/1e8)*100) + "MHz.json"
    if os.path.isfile(filenameLvlTables):
        loaddict = json.load( open( filenameLvlTables, "r"))
        #json only allows strings
        for key,value in loaddict.items():
            LvlTable[float(key)] = value

    return LvlTable

def WriteLevellingTables( freq, lvlTable):
    import json

    #TODO: Round frequency to 100 MHz - experimental; Verify frequency raster
    filenameLvlTables = "LevelTables_5GNR_" + str(round(freq/1e8)*100) + "MHz.json"
    json.dump(lvlTable, open(filenameLvlTables, "w"))

if __name__ == "__main__":
    from rssd.FSW_Common import VSA

    freq = 3e9
    FSW = VSA().jav_Open('192.168.1.108')

    table = ReadLevellingTables(freq)
    lvlTable = FSW.Set_Autolevel_IQIF(table)
    WriteLevellingTables(freq, table)
    FSW.jav_ClrErr()
    del FSW