########################################################################################################################
# M O D U L E   D O C U M E N T A T I O N : ############################################################################
########################################################################################################################


"""One of the several classification modules of "fpga4p".

This module provides class for classification model for Naive Bayes Classifier.

Function:
    start_instance: Start __init__ of the main class.

Classes:
    TrainNBC: This class provides algorithm for NBC classification.

Note:
    Every classification module must be named as '..._c' and consists
    function 'start_instance' which returns the main class instance.
"""


########################################################################################################################
# I M P O R T :  #######################################################################################################
########################################################################################################################


import fpga4p
import pandas
import pandas.errors
import serial
import serial.serialutil
import os
import pickle
from fpga4p.supporting_tools.notifications import Error, Notification
from fpga4p.supporting_tools.supporting_functions import file_name_generator, get_byte_width
from fpga4p.testing.accuracy_testing import accuracy_test
from fpga4p.supporting_tools.special_characters import *


########################################################################################################################
# M A I N   F U N C T I O N :  #########################################################################################
########################################################################################################################


def start_instance(classification_data_path, byte_word_dict, usb_device):
    """
    Returns the main class instance.
    """
    return ClassifyNBC(classification_data_path, byte_word_dict, usb_device)


########################################################################################################################
# M A I N   C L A S S :  ###############################################################################################
########################################################################################################################


class ClassifyNBC:
    """
    Classification class for Naive Bayes Classifier.

    Attributes:
        self._task: Task parameters.
        self._data_frame: .csv file for classification.
        self._byte_word_dict: Dict with word's codes.
        self._serial_port: Serial port for FPGA.
    """

    # ==================================================================================================================

    __class_path = "fpga4p.classification_algorithms.nbc_c.ClassifyNBC"

    # ==================================================================================================================

    def __init__(self, classification_data_path, byte_word_dict, serial_port):
        self._task = [classification_data_path, 'nbc_c', byte_word_dict, serial_port]
        try:
            self._data_frame = pandas.read_csv(self._task[0], sep=',', header=None)
        except FileNotFoundError:
            # If can't open classification file: -------------------------------------------------------------------
            Error(where=f'{self.__class_path}.__init__()',
                  why=f"""can't open classification file: "{self._task[0]}" in task: {self._task}""",
                  task_end=True)()
            # ----------------------------------------------------------------------------------------------------------
        except pandas.errors.EmptyDataError:
            # If classification file is empty: -------------------------------------------------------------------------
            Error(where=f'{self.__class_path}.__init__()',
                  why=f"""classification file: "{self._task[0]}" is empty in task: {self._task}""",
                  task_end=True)()
            # ----------------------------------------------------------------------------------------------------------
        else:
            try:
                word_dict_file = open(self._task[2], 'rb')
            except FileNotFoundError:
                # If can't open byte word dict file: -------------------------------------------------------------------
                Error(where=f'{self.__class_path}.__init__()',
                      why=f"""can't open byte word dict file: "{self._task[2]}" in task: {self._task}""",
                      task_end=True)()
                # ------------------------------------------------------------------------------------------------------
            else:
                # Request ROOT rights in the terminal: -----------------------------------------------------------------
                try:
                    self._byte_word_dict = pickle.load(word_dict_file)
                except pickle.PickleError:
                    # If can read for .wd file -------------------------------------------------------------------------
                    Error(where=f'{self.__class_path}.__init__()',
                          why=f"""can't read from word byte dict file: "{self._task[2]}" in task: {self._task} """,
                          task_end=True)()
                    # --------------------------------------------------------------------------------------------------

                fail = os.system('sudo chmod 666 %s' % self._task[3])
                # ------------------------------------------------------------------------------------------------------
                if not fail:
                    try:
                        self._serial_port = serial.Serial(self._task[3], 9600, timeout=1, stopbits=2)
                    except serial.serialutil.SerialException:
                        # If wrong serial port: ------------------------------------------------------------------------
                        Error(where=f'{self.__class_path}.__init__()',
                              why=f'wrong serial port "{self._task[3]}" in task: {self._task} ',
                              task_end=True)()
                        # ----------------------------------------------------------------------------------------------
                    else:
                        self.start()
                else:
                    # If ROOT rights was not obtain: -------------------------------------------------------------------
                    Error(where=f'{self.__class_path}.__init__()',
                          why=f'ROOT rights for serial port "{self._task[3]}" in task: {self._task} did not obtain',
                          task_end=True)()
                    # --------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    def start(self):
        """
        Start calculations with FPGA.
        """

        # Send notification to the notification handler: ---------------------------------------------------------------
        Notification(where=f'{self.__class_path}.start()',
                     what=f'classification task {self._task} started calculation with FPGA')()
        # --------------------------------------------------------------------------------------------------------------

        # Prepare to work with "-a" flag: ------------------------------------------------------------------------------
        real_answers = None
        fpga_answers = None
        if fpga4p.core.Core().accuracy:
            real_answers = self._data_frame[0]
            fpga_answers = []
            cols = self._data_frame.columns[:-1]
            self._data_frame = self._data_frame.drop(0, 1)
            self._data_frame.columns = cols
        # --------------------------------------------------------------------------------------------------------------

        # Prepare parameters: ------------------------------------------------------------------------------------------
        byte_list = [0xFF]
        width = get_byte_width(len(self._byte_word_dict[0]))
        # --------------------------------------------------------------------------------------------------------------

        # Create file for answers: -------------------------------------------------------------------------------------
        file_name = file_name_generator(self._task[0], '.csv', '_answers')
        while True:  # Change file name if file exists
            try:
                answers_file = open(file_name.__next__(), 'x')
            except FileExistsError:
                continue
            else:
                break
        # --------------------------------------------------------------------------------------------------------------
        print(self._byte_word_dict)
        # Generate bytes string: ---------------------------------------------------------------------------------------
        for i in range(len(self._data_frame[0])):
            row = list(self._data_frame.iloc[i, :])
            byte_list.append(int(len(row)))
            for j in range(len(row)):
                answers_file.write(str(row[j]) + ',')  # Write words in answers file
                value = int(self._byte_word_dict[0].get(str(row[j]), 0))
                width_bytes = get_byte_width(value)
                if width != width_bytes:
                    for k in range(width - width_bytes):
                        byte_list.append(0)
                byte_list.append(value)
            byte_list.append(0xFE)
        # --------------------------------------------------------------------------------------------------------------

            # Write bytes to the serial port: --------------------------------------------------------------------------
            try:
                self._serial_port.write(byte_list)
                print(byte_list)
            except serial.SerialException:
                # If can't write: --------------------------------------------------------------------------------------
                Error(where=f'{self.__class_path}.start()',
                      why=f"can't write in serial port: {self._task[3]} in task {self._task}",
                      task_end=True)()
                return 1
                # ------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------

            # Read bytes from the serial port: -------------------------------------------------------------------------
            else:
                try:
                    response = self._serial_port.read(3)
                    print(response)
                    print('\n')
                except serial.SerialException:
                    # If can't read: -----------------------------------------------------------------------------------
                    Error(where=f'{self.__class_path}.start()',
                          why=f"can't read from serial port: {self._task[3]} in task {self._task}",
                          task_end=True)()
                    # --------------------------------------------------------------------------------------------------
                    return 1
                else:
                    if not response:
                        # If answer is empty: --------------------------------------------------------------------------
                        Error(where=f'{self.__class_path}.start()',
                              why=f"answer is empty (no response) in serial port: {self._task[3]} in task {self._task}",
                              task_end=True)()
                        return 1
                        # ----------------------------------------------------------------------------------------------
                    else:
                        # Write in answers file: -----------------------------------------------------------------------
                        answer = self._byte_word_dict[1].get(response[1], 'FPGA CLASSIFICATION ERROR!')
                        answers_file.write(answer + '\n')
                        if fpga4p.core.Core().accuracy:  # Forming fpga_answers with "-a" flag
                            fpga_answers.append(answer)
                        # ----------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            byte_list = [0xFF]
        # Count accuracy: ----------------------------------------------------------------------------------------------
        if fpga4p.core.Core().accuracy:
            accuracy = accuracy_test(real_answers, fpga_answers)

            Notification(where=f'{self.__class_path}.start()',  # Send notification to the notification handler
                         what=f'The accuracy of the task {self._task} =='
                         f' {UNDERLINE_ON}{GREEN}{accuracy}{UNDERLINE_OFF}{RESET} %')()
        # ------------------------------------------------------------------------------------------------------------

        # Send notification to the notification handler: ---------------------------------------------------------------
        Notification(where=f'{self.__class_path}.start()',
                     what=f'classification task {self._task} finished',
                     task_end=True)()
        # --------------------------------------------------------------------------------------------------------------

    # ==================================================================================================================


########################################################################################################################
# E N D   O F   F I L E .  #############################################################################################
########################################################################################################################
