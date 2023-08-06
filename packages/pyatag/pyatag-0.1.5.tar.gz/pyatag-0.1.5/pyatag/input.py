"""Base data to initiate an AtagDataStore."""

TESTDATA = {
    "_host": "atag.local",  # atag IP
    "_port": 10000,
    "_mail": "matsnelissen@gmail.com",  # email registered in portal
    "_scan_interval": 30,
    "_interface": "{62AC90E3-2251-4463-B26B-CBAA14D4D2D8}",  # interface on which API runs
    "_sensors": [  # sensors to test, see const.py
        "temperature",
        "current_temp"
    ]
}
