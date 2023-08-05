import json
import os
import sys

class Signals():

    signal_index = {
        0: 'RIP',
        1: 'SVC',
        2: 'HRA',
        3: 'MRA',
        4: 'LRA',
        5: 'RV',
        6: 'RVW',
        14: 'IVC',
        16: 'PA',
        26: 'RVW_PACED'
    }

    def __init__(self):
        json_file = os.path.abspath('{}/signals.json'.format(__file__))

        with open(json_file) as f:
            self.ecg_signals = json.load(f)

    def get_signal(self, location, rate, version=0):
        signal = self.ecg_signals[location][version]

        x = signal['x'].copy()
        y = signal['y'].copy()

        if not location == 'RIP':
            y[-1] = y[0]
            time_beat = x[-1] - x[0]
            r = 1 / (rate/60)

            if r > time_beat:
                x.append(x[0] + r)
                x = [xx - x[0] for xx in x]
                y.append(y[-1])
            else:
                length = x[-1] - x[0]
                d = r / length
                x.append(x[0])
                x = [xx * d for xx in x]
                x = [xx - x[0] for xx in x]

        return x, y

if __name__ == "__main__":
    signals = Signals()

    [x,y] = signals.get_signal('SVC', 20)
    print(len(x))
    print(x[-1])
    print(x[-2])

    print(signals.get_signal('SVC', 20))
    print(signals.get_signal('SVC', 80))
    print(signals.get_signal('SVC', 140))
