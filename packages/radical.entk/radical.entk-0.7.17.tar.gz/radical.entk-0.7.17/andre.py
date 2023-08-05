
import os
import sys
import time

from radical.entk import Pipeline, Stage, Task, AppManager


hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port     = os.environ.get('RMQ_PORT', 5672)


# ------------------------------------------------------------------------------
#
def generate_pipeline():

    p  = Pipeline()
    s1 = Stage()

    start = time.time()
    for i in range(1024*1024):
        t = Task()
        t.executable = ['/bin/true']
        s1.add_tasks(t)

    stop = time.time()
    print  'time: %.2f' % (stop - start)

    p.add_stages(s1)

    return p


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    pipelines = []

    for cnt in range(1):
        pipelines.append(generate_pipeline())

    sys.exit(0)

    appman = AppManager(hostname=hostname, port=port)

    res_dict = {
        'resource': 'local.localhost',
        'walltime': 10,
        'cpus'    : 10
    }

    appman.resource_desc = res_dict
    appman.workflow      = set(pipelines)
    appman.run()


# ------------------------------------------------------------------------------

