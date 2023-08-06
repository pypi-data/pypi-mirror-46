########################################################################################################################
# M O D U L E   D O C U M E N T A T I O N : ############################################################################
########################################################################################################################


"""
One of the several training modules of "fpga4p".

This module provides class for training model for Naive Bayes Classifier.

Function:
    start_instance: Start __init__ of the main class.

Classes:
    TrainNBC: This class provides algorithm for NBC training.

Note:
    Every training module must be named as '..._t' and consists
    function 'start_instance' which returns the main class instance.
"""


########################################################################################################################
# I M P O R T :  #######################################################################################################
########################################################################################################################


import multiprocessing
import pandas
import pandas.errors
import fpga4p
import os
import os.path
import pickle
import math
import tarfile
import inspect
from fpga4p.supporting_tools.supporting_functions import file_name_generator, get_byte_width, to_int_hex_format
from fpga4p.supporting_tools.notifications import Error, Notification


########################################################################################################################
# M A I N   F U N C T I O N :  #########################################################################################
########################################################################################################################


def start_instance(train_data_path):
    """
    Returns the main class instance.
    """
    return TrainNBC(train_data_path)


########################################################################################################################
# M A I N   C L A S S :  ###############################################################################################
########################################################################################################################


class TrainNBC(multiprocessing.Process):
    """
    Training class for Naive Bayes Classifier.

    Attributes:
        self._task: Task parameters.
        self._data_frame: .csv file for training.
        self._word_dict: Dict with word's codes.
        self._class_dict: Dict with class's codes.
        self._v_l_c: Model parameter log(v + l_c).
        self._d_c: Model parameter log(d_c).
        self._w_c: Model parameter log(w_c + 1).
    """

    # ==================================================================================================================

    __class_path = "fpga4p.training_algorithms.nbc_t.TrainNBC"

    # ==================================================================================================================

    def __init__(self, training_data_path):
        super().__init__()
        self._task = [training_data_path, 'nbc_t']
        try:
            self._data_frame = pandas.read_csv(training_data_path, sep=',', header=None)
        except FileNotFoundError:
            # If can't open training.csv file: -------------------------------------------------------------------------
            Error(where=f'{self.__class_path}.__init__()',
                  why=f"""can't open training file: "{self._task[0]}" in task: {self._task}""",
                  task_end=True)()
            # ----------------------------------------------------------------------------------------------------------
        except pandas.errors.EmptyDataError:
            # If training.csv file is empty: ---------------------------------------------------------------------------
            Error(where=f'{self.__class_path}.__init__()',
                  why=f"""training file: "{self._task[0]}" is empty in task: {self._task}""",
                  task_end=True)()
            # ----------------------------------------------------------------------------------------------------------

        else:
            # Attributes bounded with supporting goals: ----------------------------------------------------------------
            self.daemon = True  # Process's attribute
            self._word_dict = {}
            self._class_dict = {}
            self._data_files_list = []
            # ----------------------------------------------------------------------------------------------------------

            # Attributes bounded with training model: ------------------------------------------------------------------
            self._v_l_c = []  # log(v + l_c)
            self._d_c = []  # log(d_c)
            self._w_c = []  # log(w_c + 1)
            # ----------------------------------------------------------------------------------------------------------

            # Calculation starts automatically with execution __init__: ------------------------------------------------
            self.start()
            # ----------------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    def _create_word_dict(self):
        """
        Create .wd byte file.
        """

        # Encode words and classes with natural numbers: ---------------------------------------------------------------
        unique_words = self._data_frame.iloc[:, 1:].stack().unique()
        unique_classes = self._data_frame[0].unique()
        self._word_dict = {str(word): number for number, word in enumerate(unique_words, start=1)}
        self._class_dict = {number: str(cls) for number, cls in enumerate(unique_classes)}
        # --------------------------------------------------------------------------------------------------------------

        # Create byte word dict file: ----------------------------------------------------------------------------------
        file_name = file_name_generator(self._task[0], '.wd')
        while True:  # Change file name if file exists
            try:
                pickle_file = open(file_name.__next__(), 'xb')
            except FileExistsError:
                continue
            else:
                break
        # --------------------------------------------------------------------------------------------------------------

        # Dump data with pickle: ---------------------------------------------------------------------------------------
        pickle.dump([self._word_dict, self._class_dict], pickle_file)
        pickle_file.close()
        # --------------------------------------------------------------------------------------------------------------

        # Send notification to the notification handler: ---------------------------------------------------------------
        Notification(where=f'{self.__class_path}._create_word_dict()',
                     what=f'byte word dict created in task {self._task}',
                     for_verbose=True)()
        # --------------------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    def _create_model_data_tar(self):
        """
        Create .tar file with model data.
        """

        # Create .tar data archive: ------------------------------------------------------------------------------------
        file_name = file_name_generator(self._task[0], '.tar', '_data')
        while True:  # Change file name if file exists
            try:
                tar_file = tarfile.open(file_name.__next__(), 'x')
            except FileExistsError:
                continue
            else:
                break
        # --------------------------------------------------------------------------------------------------------------

        data_file_d = open('data_log_D.dat', 'w')
        data_file_v = open('data_log_V.dat', 'w')
        for i in range(len(self._class_dict)):
            data_file = open(f'data_log_W_{i}.dat', 'w')
            # Write d_c and v_l_c: -------------------------------------------------------------------------------------
            data_file_d.write(self._d_c[i] + '\n')
            data_file_v.write(self._v_l_c[i] + '\n')
            # ----------------------------------------------------------------------------------------------------------
            for j in range(len(self._word_dict) + 1):
                # Write w_c: -------------------------------------------------------------------------------------------
                data_file.write(self._w_c[i].get(j, '0') + '\n')
                # ------------------------------------------------------------------------------------------------------

            # Add to .tar archive: -------------------------------------------------------------------------------------
            data_file.close()
            self._data_files_list.append(f'data_log_W_{i}.dat')
            tar_file.add(f'data_log_W_{i}.dat')
            os.remove(f'data_log_W_{i}.dat')
            # ----------------------------------------------------------------------------------------------------------

        # Add to .tar archive: -----------------------------------------------------------------------------------------
        data_file_d.close()
        data_file_v.close()
        tar_file.add('data_log_D.dat')
        tar_file.add('data_log_V.dat')
        os.remove('data_log_D.dat')
        os.remove('data_log_V.dat')
        tar_file.close()
        # --------------------------------------------------------------------------------------------------------------

        # Send notification to the notification handler: ---------------------------------------------------------------
        Notification(where=f'{self.__class_path}._create_model_data_tar()',
                     what=f'model data .tar created in task {self._task}',
                     for_verbose=True)()
        # --------------------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    def _create_sv_file(self):
        """"
        Create System Verilog file.
        """

        # Open file with System Verilog code: --------------------------------------------------------------------------
        sv_file = open(os.path.dirname(inspect.getfile(fpga4p.training_algorithms.nbc_t)) + '/nbc_verilog.sv', 'r')
        # --------------------------------------------------------------------------------------------------------------

        # Create new System Verilog code file: -------------------------------------------------------------------------
        file_name = file_name_generator(self._task[0], '.sv', '_sv_code')
        while True:  # Change file name if file exists
            try:
                new_sv_file = open(file_name.__next__(), 'x')
            except FileExistsError:
                continue
            else:
                break
        # --------------------------------------------------------------------------------------------------------------

        # Prepare parameters: ------------------------------------------------------------------------------------------
        amount_class = len(self._class_dict)
        width_fifo_rx = get_byte_width(len(self._word_dict)) * 8
        data_string = '{'
        for data_file in self._data_files_list:  # Format data string
            data_string = data_string + f'"{data_file}",' + '\n' + ' ' * 56
        data_string = data_string[:-58] + '\n' + ' ' * 55 + '}'
        # --------------------------------------------------------------------------------------------------------------

        # Change System Verilog code for concrete model: ---------------------------------------------------------------
        for line in sv_file:
            if line == f'    parameter AMOUNT_CLASS                          = x,\n':
                new_sv_file.write(f"    parameter AMOUNT_CLASS                          = "
                                  f"{amount_class},\n")
            elif line == '    parameter WIDTH_FIFO_RX                         = x,\n':
                new_sv_file.write(f"    parameter WIDTH_FIFO_RX                         = "
                                  f"{width_fifo_rx},\n")
            elif line == "    parameter string  INIT_MEM_CAL[AMOUNT_CLASS-1:0]= '{ },\n":
                new_sv_file.write(f"    parameter string  INIT_MEM_CAL[AMOUNT_CLASS-1:0]= '{data_string},\n")
            else:
                new_sv_file.write(line)
        new_sv_file.close()
        sv_file.close()
        # --------------------------------------------------------------------------------------------------------------

        # Send notification to the notification handler: ---------------------------------------------------------------
        Notification(where=f'{self.__class_path}._create_sv_file()',
                     what=f'.sv file created in task {self._task}',
                     for_verbose=True)()
        # --------------------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    def _count_v_l_c(self):
        """
        Model parameter counting.
        """
        v = len(self._word_dict)
        for i in range(len(self._class_dict)):
            l_c = self._data_frame.groupby([0]).count().sum(axis=1)[self._class_dict.get(i)]
            self._v_l_c.append(to_int_hex_format(math.log(v + l_c)))

    # ==================================================================================================================

    def _count_d_c(self):
        """
        Model parameter counting.
        """
        values = self._data_frame.groupby([0]).size()
        for i in range(len(self._class_dict)):
            d_c = values[self._class_dict.get(i)]
            self._d_c.append(to_int_hex_format(math.log(d_c)))

    # ==================================================================================================================

    def _count_w_c(self):
        """
        Model parameter counting.
        """
        for i in range(len(self._class_dict)):
            stacked = self._data_frame.loc[self._data_frame[0] == self._class_dict.get(i)].iloc[:, 1:].stack()
            stacked = stacked.apply(str)
            temporary_dict = stacked.value_counts().to_dict()
            new_dict = {}
            for word in temporary_dict:
                value = temporary_dict.get(word)
                new_dict[self._word_dict.get(word)] = to_int_hex_format(math.log(value + 1))
            self._w_c.append(new_dict)

    # ==================================================================================================================

    def run(self):
        """
        Count model in separate process.
        """

        # Send notification to the notification handler: ---------------------------------------------------------------
        Notification(where=f'{self.__class_path}.run()',
                     what=f'training task {self._task} started')()
        # --------------------------------------------------------------------------------------------------------------
        self._create_word_dict()
        # Count model parameters: --------------------------------------------------------------------------------------
        self._count_w_c()
        self._count_d_c()
        self._count_v_l_c()
        # --------------------------------------------------------------------------------------------------------------
        self._create_model_data_tar()
        self._create_sv_file()
        # Send notification to the notification handler: ---------------------------------------------------------------
        Notification(where=f'{self.__class_path}.run()',
                     what=f'training task {self._task} finished',
                     task_end=True)()
        # --------------------------------------------------------------------------------------------------------------

    # ==================================================================================================================


########################################################################################################################
# E N D   O F   F I L E .  #############################################################################################
########################################################################################################################
