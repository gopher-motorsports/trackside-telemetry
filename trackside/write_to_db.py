import InfluxWriterTemp as iw
import datetime

wrtr = iw.InfluxWriterTemp()
time = datetime.datetime.utcnow().isoformat()
body = [
    {
        "measurement": "system",
        "time": time,
        "fields": {
            "sensor": "test_sensor",
            "value": 3.14,
            "Message": "test_message",
            "MetadataID": 0
        }
    }
]
wrtr.write(body)