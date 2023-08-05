#!/usr/bin/env python

import os
import time

import radical.entk  as re
import radical.utils as ru


RMQ_PORT = int(os.environ.get('RMQ_PORT', 32769))

profiler = ru.Profiler('radical.entk.app')


def prof(event, state, uid, msg=''):
    profiler.prof(event=event, state=state, uid=uid, 
                  msg="pid:%d %s" % (os.getpid(), msg))


# ------------------------------------------------------------------------------
#
class Exchange(re.AppManager):

    def __init__(self):


        self._log = ru.Logger(name='radical.repex.exc', level='DEBUG')

        re.AppManager.__init__(self, autoterminate=False, port=RMQ_PORT) 
        self.resource_desc = {"resource" : 'local.localhost',
                              "walltime" : 30,
                              "cpus"     : 4}                                

        self._replicas  = list()
        self._waitlist  = list()

        for i in range(2):

            replica = Replica(self, self._log)
            self._replicas.append(replica)

        r0 = self._replicas[0]
        r1 = self._replicas[1]

        prof('app_create', state=r0.state, uid=r0.uid, msg='p0 (MD, EX): %s' % r0.xid)
        prof('app_create', state=r1.state, uid=r1.uid, msg='p1 (MD    ): %s' % r1.xid)


    # --------------------------------------------------------------------------
    #
    def execute(self):

        # run the replica pipelines
        self._log.debug('exc repex')
        self.workflow = set(self._replicas)
        self.run() 


    # --------------------------------------------------------------------------
    #
    def terminate(self):

        self._log.debug('exc term')
        self.resource_terminate()


    # --------------------------------------------------------------------------
    #
    def after_md(self, replica):

        prof('app_after_md', state=replica.state, uid=replica.uid)
        self._log.debug('=== EX %s after_md >>>>', replica.uid)
        # mark this replica for the next exchange
        self._waitlist.append(replica)

      # self._log.debug('=== EX %s after_md', replica.uid)

      # if len(self._waitlist) < 2:
        if replica.xid != self._replicas[0].xid:

            # suspend all but first replica
            self._log.debug('=== EX %s suspend', replica.uid)
            prof('app_suspend', state=replica.state, uid=replica.xid)
            replica.suspend()
            prof('app_suspend_ok', state=replica.state, uid=replica.xid)

        else:
            # first replica continunes and will resume all others in post_exec
            self._log.debug('=== EX %s exchange', replica.uid)

            task = re.Task()
            task.name       = 'extsk'
            task.executable = 'sleep 3'

            stage = re.Stage()
            stage.add_tasks(task)
            stage.post_exec = replica.after_ex
            time.sleep(5)

            replica.add_stages(stage)
            prof('app_add_ex', state=replica.state, uid=replica.xid, msg='%s:%s' % (stage.xid, task.xid))

        self._log.debug('=== EX %s after_md <<<<', replica.uid)


    # --------------------------------------------------------------------------
    #
    def after_ex(self, replica):

        prof('app_after_ex', state=replica.state, uid=replica.xid, 
                msg=' '.join([r.xid for r in self._replicas]))
        self._log.debug('=== EX %s after_ex >>>>', replica.uid)

        for _replica in self._replicas:

            if _replica.uid != replica.uid:

                # only resume *other* replicas
                self._log.debug('=== EX %s resumes',  _replica.uid)
                try:
                    prof('app_resume', state=_replica.state, uid=_replica.xid)
                    _replica.resume()
                    prof('app_resume_ok', state=_replica.state, uid=_replica.xid)
                except:
                    prof('app_resume_err', state=_replica.state, uid=_replica.xid)
                    self._log.debug('=== EX %s error : %s', _replica.uid,
                            _replica.xid)

        time.sleep(5)

        for _replica in self._replicas:
            self._log.debug('=== EX %s add md', _replica.uid)
            _replica.add_md_stage()


        # let the other replicas be a little faster so that they can suspend
        self._log.debug('=== EX %s after_ex <<<<', replica.uid)


# ------------------------------------------------------------------------------
#
class Replica(re.Pipeline):

    # --------------------------------------------------------------------------
    #
    def __init__(self, exchange, log):

        self._ex  = exchange
        self._log = log
        self._cnt = 0

        # entk pipeline initialization
        re.Pipeline.__init__(self)
        self.name = 'p_%s' % self.uid

        # add an initial md stage
        self.add_md_stage()


    # --------------------------------------------------------------------------
    #
    def add_md_stage(self):

      # self._log.debug('=== %s add md %s', self.uid, self._cnt)

        task = re.Task()
        task.name            = 'mdtsk-%s-%s' % (self.uid, self._cnt)
        task.executable      = 'sleep 3'
        task.cpu_reqs        = {'processes' : 1}

        stage = re.Stage()
        stage.add_tasks(task)
        stage.post_exec = self.after_md

        self.add_stages(stage)
        prof('app_add_md', state=self.state, uid=self.xid, msg='%s:%s' % (stage.xid, task.xid))


    # --------------------------------------------------------------------------
    #
    def after_md(self):

      # self._log.debug('=== %s after md', self.uid)

        self._cnt += 1
        self._ex.after_md(self)


    # --------------------------------------------------------------------------
    #
    def after_ex(self):

      # self._log.debug('=== %s after ex', self.uid)
        self._ex.after_ex(self)


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    exchange = Exchange()
    exchange.execute()       # run replicas and exchanges
    exchange.terminate()     # done


# ------------------------------------------------------------------------------

