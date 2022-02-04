from DLMSimulator import DLM
from utils import *


if __name__ == '__main__':

    sim = DLM(errors=.15)

    for i in range(30):
        sim.run()
        parsed = parse_packet(sim.data)

        assert type(parsed) == dict
        assert 'time' in parsed.keys()