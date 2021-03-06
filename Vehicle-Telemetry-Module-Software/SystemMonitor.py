import datetime
import psutil

measurement_name = "system"


def usage():
    # take a timestamp for this measurement
    time = datetime.datetime.utcnow()

    # collect some stats from psutil
    diskfree = psutil.disk_usage('/').free
    diskpercent = psutil.disk_usage('/').percent
    diskused = psutil.disk_usage('/').used
    mem1 = psutil.virtual_memory().percent
    mem2 = psutil.virtual_memory().free
    mem3 = psutil.virtual_memory().used
    load_0 = psutil.cpu_freq()[0]
    load_1 = psutil.cpu_percent()

    usage = str(diskfree) + "," + str(diskpercent) + "," + str(diskused) + "," + str(mem1) + "," + str(mem2) + "," + str(mem3) + "," + str(load_0) + "," + str(load_1)

    return usage

