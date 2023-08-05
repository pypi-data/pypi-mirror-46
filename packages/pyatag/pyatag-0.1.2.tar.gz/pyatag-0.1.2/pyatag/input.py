TESTDATA = {
    "_host": "atag.default.svc.cluster.local",
    "_port": 10000,
    "_mail": "matsnelissen@gmail.com",
    "_scan_interval": 30,
    "_interface":"en0",
    "_sensors": [
        "temperature",
        "current_temp"
    ]
}

atagDataStore(host=TESTDATA["_host"],
              port=TESTDATA["_port"],
              mail=TESTDATA["_mail"],
              interface=TESTDATA["_interface"],
              scan_interval=TESTDATA["_scan_interval"],
              sensors=TESTDATA["_sensors"])