########################################################################################################################
# M O D U L E   D O C U M E N T A T I O N : ############################################################################
########################################################################################################################


"""
Control module of "fpga4p".

This module provides execution of the tasks in the separate processes and
 synchronized output in the terminal. Performs separation of the training
 set if the "-s" flag was passed. Automatically determines which module
 should execute the task.

Classes:
    Core: The main control class.
"""


########################################################################################################################
# I M P O R T :  #######################################################################################################
########################################################################################################################


import singleton_decorator
import serial.tools.list_ports
import multiprocessing
import threading
import fpga4p
import pandas
import random
import pandas.errors
from sklearn.model_selection import train_test_split
from fpga4p.supporting_tools.notifications import Error, Notification
from fpga4p.supporting_tools.supporting_functions import arguments_extract, file_name_generator


########################################################################################################################
# M A I N   C L A S S :  ###############################################################################################
########################################################################################################################


@singleton_decorator.singleton
class Core:
    """
    The main control class.

    This class provides execution of the tasks in the separate processes and
     synchronized output in the terminal. Automatically determines which module
     should execute the task.

    Attributes:
        self._kwargs: Task strings from the terminal.
        self._manager: The Manager for synchronization.
        self._queue: The queue for notifications and errors.
        self._notification_event: Event of new notification.
        self._notification_thread: The thread for notification handling.
        self._classify_task_dict: The queue of classification tasks.
        self._task_counter: Task counter for stopping notification loop.
    """

    # ==================================================================================================================

    __class_path = "fpga4p.core.Core"

    # ==================================================================================================================

    # ==================================================================================================================

    def __init__(self, **kwargs):
        # Attributes bounded with tasks execution: ---------------------------------------------------------------------
        self._kwargs = kwargs
        self._classification_task_dict = {}
        for port in serial.tools.list_ports.comports():  # Declaration of task queues for different FPGAs
            self._classification_task_dict[port.device] = []
        # --------------------------------------------------------------------------------------------------------------

        # Attributes bounded with notification handler: ----------------------------------------------------------------
        self._manager = multiprocessing.Manager()
        self._notification_queue = self._manager.list()
        self._notification_event = self._manager.Event()
        self._notification_thread = threading.Thread(target=self._notification_handler)
        self._task_counter = multiprocessing.Value('i', 0)  # Synchronized value
        # --------------------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    @property
    def verbose(self):
        """
        Getter for "-v" parameter.
        """
        return self._kwargs.get('v')

    # ==================================================================================================================

    @property
    def classification(self):
        """
        Getter for "-c" parameter.
        """
        return self._kwargs.get('c')

    # ==================================================================================================================

    @property
    def training(self):
        """
        Getter for "-t" parameter.
        """
        return self._kwargs.get('t')

    # ==================================================================================================================

    @training.setter
    def training(self, value):
        """
        Setter for "-t" parameter after splitting with -s flag.
        """
        self._kwargs['t'] = value

    # ==================================================================================================================

    @property
    def split(self):
        """
        Getter for "-s" parameter.
        """
        return self._kwargs.get('s')

    # ==================================================================================================================

    @property
    def accuracy(self):
        """
        Getter for "-a" parameter.
        """
        return self._kwargs.get('a')

    # ==================================================================================================================

    @property
    def _next_notification(self):
        """
        Get notification or error instance from the notification queue.
        """

        # Check if notification queue is empty: ------------------------------------------------------------------------
        try:
            notification = self._notification_queue.pop(0)
        # --------------------------------------------------------------------------------------------------------------

        # If it is, unset notification event and return None: ----------------------------------------------------------
        except IndexError:
            self._notification_event.clear()
            return None
        # --------------------------------------------------------------------------------------------------------------
        else:
            return notification

    # ==================================================================================================================

    def print_notification(self, notification):
        """
        Send notification or error instance to the notification queue.
        """
        self._notification_queue.append(notification)
        self._notification_event.set()

    # ==================================================================================================================

    def start(self):
        """
        Start tasks executing in separate processes.
        """

        # Start notification handler in the separate thread: -----------------------------------------------------------
        self._task_counter.value += 1  # Notification handler consider as one of the tasks
        self._notification_thread.start()
        # --------------------------------------------------------------------------------------------------------------

        # Check too few arguments error: -------------------------------------------------------------------------------
        if self.training is None and self.classification is None:
            Error(where=f'{self.__class_path}.start()',
                  why='too few arguments',
                  fatal=True,
                  task_end=True)()
        # --------------------------------------------------------------------------------------------------------------

        # If "-s" flag was given: --------------------------------------------------------------------------------------
        if self.split and self.training is not None:
            self._split_samples(self.training)  # Splitting samples 70/30
        # --------------------------------------------------------------------------------------------------------------

        # Extract arguments from the training task strings: ------------------------------------------------------------
        if self.training:
            for arg in arguments_extract(self.training):
                # Every training task must have exactly 2 arguments: ---------------------------------------------------
                if len(arg) != 2:
                    Error(where=f'{self.__class_path}.start()',
                          why=f'wrong number of arguments for training task: {arg}')()
                # ------------------------------------------------------------------------------------------------------
                else:
                    self._start_training(arg[0], arg[1])
        # --------------------------------------------------------------------------------------------------------------

        # Extract arguments from the classification task strings: ------------------------------------------------------
        if self.classification:
            for arg in arguments_extract(self.classification):
                # Every classification task must have exactly 4 arguments: ---------------------------------------------
                if len(arg) != 4:
                    Error(where=f'{self.__class_path}.start()',
                          why=f'wrong number of arguments for classification task: {arg}')()
                # ------------------------------------------------------------------------------------------------------
                else:
                    self._add_classification_queue(arg[0], arg[1], arg[2], arg[3])
        # --------------------------------------------------------------------------------------------------------------

        # Execute separate process for task queue for every FPGA: ------------------------------------------------------
        for task_queue in self._classification_task_dict.values():
            classification_process = multiprocessing.Process(target=self._start_classification_queue,
                                                             args=(task_queue,))
            classification_process.daemon = True
            classification_process.start()
        # --------------------------------------------------------------------------------------------------------------

        # Send notification to the notification handler: ---------------------------------------------------------------
        Notification(where=f'{self.__class_path}.start()',
                     what='all tasks started',
                     task_end=True,
                     for_verbose=True)()
        # --------------------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    def _notification_handler(self):
        """
        This loop handles notifications and errors from queue.
        """
        while self._task_counter.value != 0:  # Endless loop, while not all tasks are finished
            # Waiting for new notification: ----------------------------------------------------------------------------
            self._notification_event.wait()
            # ----------------------------------------------------------------------------------------------------------

            # Print new notification: ----------------------------------------------------------------------------------
            notification = self._next_notification
            if notification is None:
                continue
            else:
                # Check if the notification is for verbose mode only: --------------------------------------------------
                if self.verbose:
                    notification.output()
                elif not notification.for_verbose:
                    notification.output()
                # ------------------------------------------------------------------------------------------------------

                # Subtract 1 from the task counter if the task finished: -----------------------------------------------
                if notification.task_end:
                    self._task_counter.value += -1
                # ------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    def _start_training(self, training_data_path, training_class):
        """
        Execute the training task.
        """
        self._task_counter.value += 1
        # Try to find passed training class: ---------------------------------------------------------------------------
        try:
            train_module = getattr(fpga4p.training_algorithms, training_class)
        # --------------------------------------------------------------------------------------------------------------
        except AttributeError:
            # If passed training class is unavailable: -----------------------------------------------------------------
            Error(where=f'{self.__class_path}._start_training()',
                  why=f'wrong training class "{training_class}" in task: {[training_data_path, training_class]}',
                  task_end=True)()
            # ----------------------------------------------------------------------------------------------------------
        else:
            train_module.start_instance(training_data_path)  # Training classes inherits multiprocessing.Process

    # ==================================================================================================================

    def _add_classification_queue(self, classification_data_path, classification_class, byte_word_dict, serial_port):
        """
        Append classification task in the queue for concrete FPGA.
        """
        self._task_counter.value += 1
        task = [classification_data_path, classification_class, byte_word_dict, serial_port]
        # Try to find passed serial port: ------------------------------------------------------------------------------
        try:
            task_list = self._classification_task_dict[task[3]]
        # --------------------------------------------------------------------------------------------------------------
        except KeyError:
            # If passed unavailable serial port: -----------------------------------------------------------------------
            Error(where=f'{self.__class_path}._add_classification_queue()',
                  why=f'wrong serial port "{task[3]}" in task: {task}',
                  task_end=True)()
            # ----------------------------------------------------------------------------------------------------------
        else:  # Classification tasks are still not executed
            task_list.append(task)

    # ==================================================================================================================

    def _start_classification_queue(self, task_queue):
        """
        Start separate process for calculation of tasks queue with concrete FPGA.
        """
        for task in task_queue:  # This queue consists tasks for one concrete FPGA
            # Try to find passed classification class: -----------------------------------------------------------------
            try:
                classification_module = getattr(fpga4p.classification_algorithms, task[1])
            # ----------------------------------------------------------------------------------------------------------
            except AttributeError:
                # If passed classification class is unavailable: -------------------------------------------------------
                Error(where=f'{self.__class_path}._start_classification_queue()',
                      why=f'wrong classification class "{task[1]}" in task: {task}',
                      task_end=True)()
                # ------------------------------------------------------------------------------------------------------
            else:  # Start separate process for calculation of tasks queue with concrete FPGA
                classification_module.start_instance(task[0], task[2], task[3])

    # ==================================================================================================================

    def _split_samples(self, training_task_string):
        """
        Divides the training set into parts 70/30.
        """
        new_training_task_string = ''
        # Send notification to the notification handler: ---------------------------------------------------------------
        Notification(where=f'{self.__class_path}._split_samples()',
                     what=f'start splitting training samples',
                     for_verbose=True)()
        # --------------------------------------------------------------------------------------------------------------

        for arg in arguments_extract(training_task_string):
            try:
                data_frame = pandas.read_csv(arg[0], sep=',', header=None)
            except FileNotFoundError:
                # If can't open training data file: --------------------------------------------------------------------
                Error(where=f'{self.__class_path}._split_samples()',
                      why=f"""can't open training file: "{arg[0]}" in task: {arg}""")()
                # ------------------------------------------------------------------------------------------------------
            except pandas.errors.EmptyDataError:
                # If training data file is empty: ----------------------------------------------------------------------
                Error(where=f'{self.__class_path}._split_samples()',
                      why=f"""training file: "{arg[0]}" is empty in task: {arg}""")()

                # ------------------------------------------------------------------------------------------------------
            else:
                # Divide the training sample: --------------------------------------------------------------------------
                df_train, df_test = train_test_split(data_frame, test_size=0.3, random_state=random.randint(1, 100))
                # ------------------------------------------------------------------------------------------------------

                # Create two new .csv files: ---------------------------------------------------------------------------
                train_file_name = file_name_generator(arg[0], '.csv', '_TRAIN70')
                while True:  # Change file name if file exists
                    try:
                        train_file = open(train_file_name.__next__(), 'x')
                    except FileExistsError:
                        continue
                    else:
                        break

                test_file_name = file_name_generator(arg[0], '.csv', '_TEST30')
                while True:  # Change file name if file exists
                    try:
                        test_file = open(test_file_name.__next__(), 'x')
                    except FileExistsError:
                        continue
                    else:
                        break
                # ------------------------------------------------------------------------------------------------------

                # Write split samples: ---------------------------------------------------------------------------------
                df_train.to_csv(train_file, index=False, header=False, )
                df_test.to_csv(test_file, index=False, header=False)
                test_file.close()
                train_file.close()
                # ------------------------------------------------------------------------------------------------------

                # Send notification to the notification handler: -------------------------------------------------------
                Notification(where=f'{self.__class_path}._split_samples()',
                             what=f'training samples were split in task {arg}',
                             for_verbose=True)()
                # ------------------------------------------------------------------------------------------------------
                arg[0] = train_file.name
                new_training_task_string = new_training_task_string + ','.join(arg) + ';'

        self.training = new_training_task_string[:-1]

    # ==================================================================================================================

########################################################################################################################
# E N D   O F   F I L E .  #############################################################################################
########################################################################################################################
