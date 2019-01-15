
def confSetLight(ledAmountMoisture, ledAmountLight, ledAmountTemperature):
    moistureRemainder = 14 - ledAmountMoisture
    lightRemainder = 11 - ledAmountLight
    temperatureRemainder = 9 - ledAmountTemperature

    data = moistureRemainder * [(0,0,0)] + ledAmountMoisture * [(101,30,145)] + lightRemainder * [(0,0,0)] + ledAmountLight * [(200,255,30)] + temperatureRemainder * [(0,0,0)] + ledAmountTemperature * [(60, 255, 30)]

    return data
