import sys
import traceback

import numpy as np
from numpy import argmin, array, sqrt, sum


def what_the_fuck():
    a = np.arange(1, 10)
    b = 10**np.arange(4)
    (b[:, np.newaxis] * a).flatten()


def callstack_prompt(from_traceback):
    while True:
        resp = input("Show callstack? (y/N) ").strip()

        if resp in {'y', 'Y', 'n', 'N'} or len(resp) == 0:
            if resp in {'y', 'Y'}:
                traceback.print_tb(from_traceback)
            break

        print("Invalid input. Please try again.")


if __name__ == '__main__':
    try:
        what_the_fuck()
        print("Done.")
    except Exception as e:
        print(sys.exc_info()[1])
        callstack_prompt(sys.exc_info()[2])


observation = array([111.0, 188.0])
codes = array([[102.0, 203.0],
               [132.0, 193.0],
               [45.0, 155.0],
               [57.0, 173.0]])
diff = codes - observation    # the broadcast happens here
dist = sqrt(sum(diff**2, axis=-1))
argmin(dist)
