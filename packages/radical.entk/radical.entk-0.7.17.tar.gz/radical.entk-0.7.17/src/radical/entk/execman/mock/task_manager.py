__copyright__ = "Copyright 2017-2018, http://radical.rutgers.edu"
__author__ = "Vivek Balasubramanian <vivek.balasubramaniana@rutgers.edu>"
__license__ = "MIT"

import radical.utils as ru
from radical.entk.exceptions import EnTKError
import threading
from multiprocessing import Process, Event
from radical.entk import states, Task
import time
import json
import pika
import traceback
import os
import uuid
from ..base.task_manager import Base_TaskManager
from radical.entk.utils.init_transition import transition
import Queue


class TaskManager(Base_TaskManager):

    """
    A Task Manager takes the responsibility of dispatching tasks it receives from a pending_queue for execution on to
    the available resources using a runtime system. Once the tasks have completed execution, they are pushed on to
    the completed_queue for other components of EnTK to process.

    :arguments:
        :pending_queue: List of queue(s) with tasks ready to be executed. Currently, only one queue.
        :completed_queue: List of queue(s) with tasks that have finished execution. Currently, only one queue.
        :rmgr: ResourceManager object to be used to access the Pilot where the tasks can be submitted
        :mq_hostname: Name of the host where RabbitMQ is running
        :port: port at which rabbitMQ can be accessed

    Currently, EnTK is configured to work with one pending queue and one completed queue. In the future, the number of
    queues can be varied for different throughput requirements at the cost of additional Memory and CPU consumption.
    """

    def __init__(self, sid, pending_queue, completed_queue,
                 rmgr, mq_hostname, port):

        super(TaskManager, self).__init__(sid,
                                          pending_queue,
                                          completed_queue,
                                          rmgr,
                                          mq_hostname,
                                          port,
                                          rts='mock')

        self._rmq_ping_interval = os.getenv('RMQ_PING_INTERVAL', 10)

        self._logger.info('Created task manager object: %s' % self._uid)
        self._prof.prof('tmgr obj created', uid=self._uid)

    # ------------------------------------------------------------------------------------------------------------------
    # Private Methods
    # ------------------------------------------------------------------------------------------------------------------

    def _tmgr(self, uid, rmgr, logger, mq_hostname, port, pending_queue, completed_queue):
        """
        **Purpose**: Method to be run by the tmgr process. This method receives a Task from the pending_queue
        and submits it to the RTS. Currently, it also converts Tasks into CUDs and CUs into (partially described) Tasks.
        This conversion is necessary since the current RTS is RADICAL Pilot. Once Tasks are recovered from a CU, they
        are then pushed to the completed_queue. At all state transititons, they are synced (blocking) with the AppManager
        in the master process.

        In addition the tmgr also receives heartbeat 'request' msgs from the heartbeat-req queue. It responds with a
        'response' message to the 'heartbeart-res' queue.

        **Details**: The AppManager can re-invoke the tmgr process with this function if the execution of the workflow is
        still incomplete. There is also population of a dictionary, placeholder_dict, which stores the path of each of
        the tasks on the remote machine.
        """

        try:

            def heartbeat_response(mq_channel):

                try:

                    # Get request from heartbeat-req for heartbeat response
                    hb_method_frame, hb_props, hb_body = mq_channel.basic_get(
                        queue=self._hb_request_q)

                    if hb_body:

                        logger.info('Received heartbeat request')

                        mq_channel.basic_publish(exchange='',
                                                 routing_key=self._hb_response_q,
                                                 properties=pika.BasicProperties(
                                                     correlation_id=hb_props.correlation_id),
                                                 body='response')

                        logger.info('Sent heartbeat response')
                        mq_channel.basic_ack(
                            delivery_tag=hb_method_frame.delivery_tag)

                except Exception, ex:
                    logger.exception(
                        'Failed to respond to heartbeat request, error: %s' % ex)
                    raise

            local_prof = ru.Profiler(
                name='radical.entk.%s' % self._uid + '-proc', path=self._path)

            local_prof.prof('tmgr process started', uid=self._uid)
            logger.info('Task Manager process started')

            # Thread should run till terminate condtion is encountered
            mq_connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=mq_hostname, port=port))
            mq_channel = mq_connection.channel()

            # Queue for communication between threads of this process
            task_queue = Queue.Queue()

            # Start second thread to receive tasks and push to RTS
            self._rts_runner = threading.Thread(target=self._process_tasks,
                                                args=(task_queue,
                                                      rmgr,
                                                      logger,
                                                      mq_hostname,
                                                      port,
                                                      local_prof,
                                                      self._sid))
            self._rts_runner.start()

            local_prof.prof('tmgr infrastructure setup done', uid=uid)

            last = time.time()
            while not self._tmgr_terminate.is_set():

                try:

                    method_frame, header_frame, body = mq_channel.basic_get(
                        queue=pending_queue[0])

                    if body:

                        body = json.loads(body)
                        task_queue.put(body)

                        mq_channel.basic_ack(
                            delivery_tag=method_frame.delivery_tag)

                    heartbeat_response(mq_channel)

                except Exception, ex:
                    logger.exception('Error in task execution: %s' % ex)
                    raise

        except KeyboardInterrupt:

            logger.exception('Execution interrupted by user (you probably hit Ctrl+C), ' +
                               'trying to cancel tmgr process gracefully...')

        except Exception, ex:

            logger.exception('%s failed with %s'%(self._uid, ex))
            raise EnTKError(ex)

        finally:

            local_prof.prof('terminating tmgr process', uid=uid)

            if self._rts_runner:
                self._rts_runner.join()

            mq_connection.close()
            local_prof.close()

    def _process_tasks(self, task_queue, rmgr, logger, mq_hostname, port, local_prof, sid):

        def load_placeholder(task):

            parent_pipeline = str(task.parent_pipeline['name'])
            parent_stage = str(task.parent_stage['name'])

            if parent_pipeline not in placeholder_dict:
                placeholder_dict[parent_pipeline] = dict()

            if parent_stage not in placeholder_dict[parent_pipeline]:
                placeholder_dict[parent_pipeline][parent_stage] = dict()

            if None not in [parent_pipeline, parent_stage, task.name]:
                placeholder_dict[parent_pipeline][parent_stage][str(
                    task.name)] = str(task.path)

        placeholder_dict = dict()

        mq_connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=mq_hostname, port=port))
        mq_channel = mq_connection.channel()

        try:

            while not self._tmgr_terminate.is_set():

                body = None

                try:
                    body = task_queue.get(block=True, timeout=10)
                except Queue.Empty:
                    # Ignore empty exception, we don't always have new tasks to run
                    pass

                if body:

                    task_queue.task_done()

                    bulk_tasks = list()
                    bulk_cuds = list()

                    for task in body:
                        t = Task()
                        t.from_dict(task)
                        bulk_tasks.append(t)

                        transition(obj=t,
                                   obj_type='Task',
                                   new_state=states.SUBMITTING,
                                   channel=mq_channel,
                                   queue='%s-tmgr-to-sync' % self._sid,
                                   profiler=local_prof,
                                   logger=self._logger)

                    for task in bulk_tasks:

                        transition(obj=task,
                                   obj_type='Task',
                                   new_state=states.SUBMITTED,
                                   channel=mq_channel,
                                   queue='%s-tmgr-to-sync' % self._sid,
                                   profiler=local_prof,
                                   logger=self._logger)
                        self._logger.info(
                            'Task %s submitted to RTS' % (task.uid))

                    for task in bulk_tasks:

                        transition(obj=task,
                                   obj_type='Task',
                                   new_state=states.COMPLETED,
                                   channel=mq_channel,
                                   queue='%s-cb-to-sync' % self._sid,
                                   profiler=local_prof,
                                   logger=logger)

                        task_as_dict = json.dumps(task.to_dict())

                        mq_channel.basic_publish(exchange='',
                                                 routing_key='%s-completedq-1' % self._sid,
                                                 body=task_as_dict
                                                 # properties=pika.BasicProperties(
                                                 # make message persistent
                                                 #    delivery_mode = 2,
                                                 # )
                                                 )

                        logger.info('Pushed task %s with state %s to completed queue %s-completedq-1' % (
                            task.uid,
                            task.state,
                            sid))

        except KeyboardInterrupt as ex:
            logger.exception('Execution interrupted by user (you probably hit Ctrl+C), ' +
                         'trying to cancel task processor gracefully...')

        except Exception as ex:
            logger.exception('%s failed with %s'%(self._uid, ex))
            raise EnTKError(ex)
        # ------------------------------------------------------------------------------------------------------------------
        # Public Methods
        # ------------------------------------------------------------------------------------------------------------------

    def start_manager(self):
        """
        **Purpose**: Method to start the tmgr process. The tmgr function
        is not to be accessed directly. The function is started in a separate
        thread using this method.
        """

        if not self._tmgr_process:

            try:

                self._prof.prof('creating tmgr process', uid=self._uid)
                self._tmgr_terminate = Event()

                self._tmgr_process = Process(target=self._tmgr,
                                             name='task-manager',
                                             args=(
                                                 self._uid,
                                                 self._rmgr,
                                                 self._logger,
                                                 self._mq_hostname,
                                                 self._port,
                                                 self._pending_queue,
                                                 self._completed_queue)
                                             )

                self._logger.info('Starting task manager process')
                self._prof.prof('starting tmgr process', uid=self._uid)
                self._tmgr_process.start()

                return True

            except Exception, ex:

                self._logger.exception('Task manager not started, error: %s' % ex)
                self.terminate_manager()
                raise

        else:
            self._logger.warn(
                'tmgr process already running, but attempted to restart!')

    # ------------------------------------------------------------------------------------------------------------------
