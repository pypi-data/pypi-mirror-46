#!/usr/bin/env python

import os
import time

import radical.entk as re


# ------------------------------------------------------------------------------
#

hostname =     os.environ.get('RMQ_HOSTNAME', 'localhost')
port     = int(os.environ.get('RMQ_PORT', 5672))

n_pipes  = 2
n_stages = 4
n_tasks  = 2


# ------------------------------------------------------------------------------
#
def generate_workflow():

    workflow = list()

    for i in range(n_pipes):

        p = re.Pipeline()

        for j in range(n_stages):

            s = re.Stage()

            for k in range(n_tasks):

                t = re.Task()
                t.executable = 'sleep'
                t.arguments  = ['3']

                s.add_tasks(t)

            # Add post-exec to the Stage
            def func_condition():
                p.suspend()
                print 'Suspending pipeline %s for 3 seconds' % p.uid
                time.sleep(3)
                print 'Resuming pipeline %s' % p.uid
                p.resume()

            s.post_exec = func_condition

            p.add_stages(s)

        workflow.append(p)

    return workflow


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    # Create a dictionary describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {
        'resource': 'local.localhost',
        'walltime': 15,
        'cpus'    : 2,
    }

    # Create Application Manager
    appman = re.AppManager(hostname=hostname, port=port)
    appman.resource_desc = res_dict


    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.workflow = generate_workflow()

    # Run the Application Manager
    appman.run()


# ------------------------------------------------------------------------------

