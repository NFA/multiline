
INSTRUMENT      = 0
INSTRUMENT_ID   = 1
SAMPLE_ID       = 2
DATE            = 3
SENSOR_VALUE    = 4
SENSOR_UNIT     = 5
SENSOR_QUANTITY = 6
TEMP_VALUE      = 7
TEMP_UNIT       = 8
TEMP            = 9
AUTOREAD        = 10
CALIBRATION     = 11
SENSOR_INFO     = 12
SENSOR_NAME     = 13
SENSOR_ID       = 14

SENSORS = dict()

def IDS_sensor(sensor_quantity):
    return lambda f: SENSORS.update({sensor_quantity: f})

def parse_sensor(csv):
    """ 
    Ideally, the output from the sensors would be standardized and a simple
    list to dict conversion would be possible. However, there are differences 
    between the sensors that need to be accommodated. 
    """
    lst = csv.split(";")
    sensor = lst[SENSOR_QUANTITY]

    if sensor in SENSORS:
        result = SENSORS[sensor](lst)
    else:
        result = parse_generic_sensor(lst)

    return result

def parse_generic_sensor(data):
    return sensor_data(date = data[DATE],
        quantity = data[SENSOR_QUANTITY], value = data[SENSOR_VALUE], unit = data[SENSOR_UNIT],
        temp = data[TEMP_VALUE], temp_unit = data[TEMP_UNIT],
        sensor_info = data[SENSOR_INFO], sensor_name = data[SENSOR_NAME], sensor_id = data[SENSOR_ID],
        instrument_name = data[INSTRUMENT], instrument_id = data[INSTRUMENT_ID])     

def sensor_data(date, quantity, value, unit, 
    temp, temp_unit,
    sensor_info, sensor_name, sensor_id, 
    instrument_name, instrument_id):
    """
    Single exit point of data to ensure uniform dict structure. 
    """
    return {"date": date,
        "quantity": quantity, "value": value, "unit": unit,
        "temp": temp, "temp_unit": temp_unit,
        "sensor_info": sensor_info, "sensor_name": sensor_name, "sensor_id": sensor_id,
        "instrument_name": instrument_name, "instrument_id": instrument_id
        }

@IDS_sensor("TRB")
def turbidity(data):
    """
    Deviations from normal sensor data:
        - no temperature measurement
        - no sensor info 
    """
    return sensor_data(date = data[DATE],
        quantity = "turbidity", value = data[SENSOR_VALUE], unit = data[SENSOR_UNIT],
        temp = "", temp_unit = "",
        sensor_info = "", sensor_name = data[SENSOR_NAME], sensor_id = data[SENSOR_ID],
        instrument_name = data[INSTRUMENT], instrument_id = data[INSTRUMENT_ID])

@IDS_sensor("Cond")
def conductivity(data):
    """
    Deviations from normal sensor data:
        - measures one four different quantities
    """
    possibilities = {
        "µS/cm" : "conductivity",
        "mS/cm" : "conductivity",
        "Ω·cm"  : "resistivity",
        "kΩ·cm" : "resistivity",
        "MΩ·cm" : "resistivity",
        ""      : "salinity",
        "mg/l"  : "total_dissolved_solids",
        "g/l"   : "total_dissolved_solids"
    }
    
    unit = data[SENSOR_UNIT]
    quantity = possibilities[unit]

    return sensor_data(date = data[DATE],
        quantity = quantity, value = data[SENSOR_VALUE], unit = data[SENSOR_UNIT],
        temp = data[TEMP_VALUE], temp_unit = data[TEMP_UNIT],
        sensor_info = data[SENSOR_INFO], sensor_name = data[SENSOR_NAME], sensor_id = data[SENSOR_ID],
        instrument_name = data[INSTRUMENT], instrument_id = data[INSTRUMENT_ID])

@IDS_sensor("Ox")
def dissolved_oxygen(data):
    """
    Deviations from normal sensor data:
        - measures two out of three different data points
        - there is an extra ; offsetting some of the data 
    """
    possibilities = {
        "mg/l" : "dissolved_oxygen_concentration",
        "%"    : "dissolved_oxygen_saturation",
        "mbar" : "dissolved_oxygen_partial_pressure"
    }
    quantity = possibilities[data[SENSOR_UNIT]]
        
    return sensor_data(date = data[DATE],
        quantity = quantity, value = data[SENSOR_VALUE], unit = data[SENSOR_UNIT],
        temp = data[TEMP_VALUE], temp_unit = data[TEMP_UNIT],
        sensor_info = data[SENSOR_INFO], sensor_name = data[SENSOR_NAME+1], sensor_id = data[SENSOR_ID+1],
        instrument_name = data[INSTRUMENT], instrument_id = data[INSTRUMENT_ID])
