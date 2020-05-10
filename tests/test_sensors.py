import unittest

from multiline.sensors import parse_sensor

instrument_data = [
    "Multi 3630 IDS; 19410634;1;29.04.2020 10:35:33;414.3;FNU;TRB;;;;;;;VisoTurb 900-P; 19B103894;",
    "Multi 3630 IDS; 19410634;1;29.04.2020 10:35:34;7.702;;pH;16.6;°C;Temp;;100%;;SenTix 940; C200817020;",
    "Multi 3630 IDS; 19410634;1;29.04.2020 10:35:34;183.9;µS/cm;Cond;16.5;°C;Temp;AR;;C = 0.475 1/cm   Tref25   nLF;TetraCon 925; 19411430;",
    "Multi 3630 IDS; 19410634;;15.04.2020 11:03:48;97.0;%;Ox;19.4;°C;Temp;AR;;SC-FDO   19391671;;FDO 925; 19411244;",
    "Multi 3630 IDS; 19410634;;15.04.2020 11:03:48;8.74;mg/l;Ox;19.4;°C;Temp;AR;;SC-FDO   19391671;;FDO 925; 19411244;"
]


class TestParse(unittest.TestCase):

    def test_parse_instrument_names(self):
        instrument_names = [parse_sensor(datum)["instrument_name"] for datum in instrument_data]
        self.assertEqual(instrument_names, ["Multi 3630 IDS"] * len(instrument_data))

    def test_parse_quantities(self):
        units = [parse_sensor(datum)["quantity"] for datum in instrument_data]
        self.assertEqual(units, ["turbidity", "pH", "conductivity", "dissolved_oxygen_saturation", "dissolved_oxygen_concentration"])

    def test_parse_values(self):
        values = [parse_sensor(datum)["value"] for datum in instrument_data]
        values = [float(value) for value in values]
        self.assertEqual(values, [414.3, 7.702, 183.9, 97.0, 8.74])

    def test_parse_units(self):
        units = [parse_sensor(datum)["unit"] for datum in instrument_data]
        self.assertEqual(units, ["FNU", "", "µS/cm", "%","mg/l"])
    
    def test_parse_temperatures(self):
        temps = [parse_sensor(datum)["temp"] for datum in instrument_data]
        temps = [temp for temp in temps if temp.strip()]
        temps = [float(temp) for temp in temps]
        self.assertEqual(sum(temps), 71.9)


if __name__ == "__main__":
    unittest.main()