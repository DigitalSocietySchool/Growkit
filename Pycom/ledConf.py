def confSetLight(ledAmountMoisture, ledAmountLight, ledAmountTemperature):
    #First a remainder has to be calculated. If, for example, 8 of the leds of the moisture rstrip
    # are turned on, 4 has to be turned of. These 4 leds are is the remainder.
    moistureRemainder = 14 - ledAmountMoisture
    lightRemainder = 11 - ledAmountLight
    temperatureRemainder = 9 - ledAmountTemperature

    #data will first be the remainder of the moisture leds (the remainder will be done first
    #because the ledstrip has been put backwards in the Main Hub). Then the led amount of moisture
    #is next. This goes the same for light and temperature.
    data = moistureRemainder * [(0,0,0)] + ledAmountMoisture * [(101,30,145)] + lightRemainder * [(0,0,0)] + ledAmountLight * [(200,255,30)] + temperatureRemainder * [(0,0,0)] + ledAmountTemperature * [(60, 255, 30)]

    #Return this data array and give it to the ws2812 file where the leds will be turned on.
    return data
