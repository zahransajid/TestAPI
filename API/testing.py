import numpy as np
from API.route import APIRoute
from matplotlib import pyplot as plt


def stress_expn(route: APIRoute, n_max: int, steps=10):
    req_n = np.array(np.linspace(10, n_max, steps), dtype=np.int32)
    times = []
    vals = []
    route.isBatch = True
    for n in req_n:
        route.iterator = range(n)
        times.append(np.average([r.response_time() for r in route.execute()]))
        vals.append(n)
    plt.plot(vals, times)
    plt.show()
