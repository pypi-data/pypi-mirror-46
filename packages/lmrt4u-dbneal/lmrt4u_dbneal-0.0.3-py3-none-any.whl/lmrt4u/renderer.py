# -*- coding unix -*-

import matplotlib.pyplot as plt
import asciiplotlib as apl
import numpy as np
import matplotlib.dates as mdates
import math

from pyfiglet import figlet_format

try:
    from termcolor import colored
except ImportError:
    colored = None


def renderAscii(totalPoints, completedPointArr, totalDays):
    """Prints expected and actual burndown charts to screen"""

    expectedLinear = np.linspace(totalPoints, 0, num=totalDays+1)
    actualLinear = np.array (completedPointArr)
    x = np.arange(totalDays)

    # Console plotting

    print(figlet_format("Sample Sprint", "slant"))
    fig = apl.figure()
    fig.plot(x, expectedLinear, label='Points', xlabel= "Days", title="Expected")
    fig.plot(x, actualLinear, label='Points', xlabel= "Days", title="Actual")
    fig.show()

def renderMatPlot(totalPoints, completedPointArr, totalDays):

    expectedLinear = np.linspace(totalPoints, 0, num=totalDays)
    actualLinear = completedPointArr
    x = np.arange(totalDays)

    plt.plot(x, expectedLinear, label='Expected')
    plt.plot(x, actualLinear, label='Actual')

    plt.xlabel('Time')
    plt.ylabel('Story Points')

    plt.title("Burndown Chart")

    plt.legend()

    plt.show()

if __name__ == '__main__':
    main()
