########################################################################################################################
# M O D U L E   D O C U M E N T A T I O N : ############################################################################
########################################################################################################################


"""
This module contains templates for various notifications.

This module provides classes for convenient output of notifications,
 errors and special information, marking where the notification is coming from.

Classes:
    Notification: For printing notifications.
    Error: For printing errors.
    InformationTemplate: For printing information when flag "-i" was passed.
"""


########################################################################################################################
# I M P O R T :  #######################################################################################################
########################################################################################################################


import datetime
import fpga4p
import serial.tools.list_ports
from fpga4p.supporting_tools.special_characters import *


########################################################################################################################
# M A I N   C L A S S :  ###############################################################################################
########################################################################################################################


class Notification:
    """
    Class for printing notifications.

    Args:
        self._string: Notification string.
        self._task_end: Notification about task ending.
        self._for_verbose: If notification for verbose mode only.
        self._time: Current time.
    """

    # ==================================================================================================================

    def __init__(self, where='unknown', what='unknown', task_end=False, for_verbose=False):
        # Special characters are declared in start.py
        if for_verbose:
            self._COLOR = YELLOW
        else:
            self._COLOR = GREEN
        self._time = None
        self._string = ('\n' + f'{UNDERLINE_ON} {UNDERLINE_OFF}' * 40 +
                        f'\n{self._COLOR}{UNDERLINE_ON}NOTIFICATION{UNDERLINE_OFF}{RESET}' +
                        ' |{TIME}| :' +
                        f'\n\n\t{UNDERLINE_ON}Where?{UNDERLINE_OFF}: %s' % where +
                        f'\n\t{UNDERLINE_ON}What?{UNDERLINE_OFF}: %s' % what +
                        f'\n\t{UNDERLINE_ON}Task end?{UNDERLINE_OFF}: %s ' % task_end +
                        '\n' + f'{UNDERLINE_ON} {UNDERLINE_OFF}' * 40 + '\n')
        self._task_end = task_end
        self._for_verbose = for_verbose

    # ==================================================================================================================

    @property
    def for_verbose(self):
        """
        Check if notification for verbose mode only.
        """
        return self._for_verbose

    # ==================================================================================================================

    @property
    def task_end(self):
        """
        Notification about task ending.
        """
        return self._task_end

    # ==================================================================================================================

    def output(self):
        """
        Print notification string.
        """
        print(self._string)

    # ==================================================================================================================

    def __call__(self):
        """
        Send to the notification handler.
        """

        # Set current time: --------------------------------------------------------------------------------------------
        self._time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        self._string = self._string.format(TIME=self._time)
        # --------------------------------------------------------------------------------------------------------------
        fpga4p.core.Core().print_notification(self)

    # ==================================================================================================================


########################################################################################################################
# S E C O N D A R Y   C L A S S :  #####################################################################################
########################################################################################################################


class Error(Notification):
    """
    Class for printing errors.

    Args:
        self._string: Error string.
        self._for_verbose: Always False.
        self._fatal: If need to terminate notification handler.
    """

    # ==================================================================================================================

    def __init__(self, where='unknown', why='unknown', fatal=False, task_end=False):
        # Special characters are declared in start.py
        super().__init__(task_end=task_end)
        self._string = ('\n' + f'{UNDERLINE_ON} {UNDERLINE_OFF}' * 40 +
                        f'\n{RED}{UNDERLINE_ON}ERROR{UNDERLINE_OFF}{RESET}' +
                        ' |{TIME}| :' +
                        f'\n\n\t{UNDERLINE_ON}Where?{UNDERLINE_OFF}: %s' % where +
                        f'\n\t{UNDERLINE_ON}Why?{UNDERLINE_OFF}: %s' % why +
                        f'\n\t{UNDERLINE_ON}Fatal?{UNDERLINE_OFF}: %s ' % fatal +
                        f'\n\t{UNDERLINE_ON}Task end?{UNDERLINE_OFF}: %s ' % task_end +
                        '\n\n' + f'{UNDERLINE_ON} {UNDERLINE_OFF}' * 40 + '\n')
        self._fatal = fatal

    # ==================================================================================================================

    def output(self):
        """
        Print error string.
        """
        print(self._string)
        if self._fatal:
            exit(1)  # Exit from notification handler if error is fatal

    # ==================================================================================================================

########################################################################################################################
# S E C O N D A R Y   C L A S S :  #####################################################################################
########################################################################################################################


class InformationTemplate:

    # ==================================================================================================================

    def __init__(self):
        self._name_list = ['AVAILABLE TRAINING ALGORITHMS',
                           'AVAILABLE CLASSIFICATION ALGORITHMS',
                           'AVAILABLE SERIAL USB PORTS']
        self._type_list = ['ALGORITHM',
                           'ALGORITHM',
                           'SERIAL PORT']
        self._iterators_list = [filter(lambda x: x[-2:] == '_t', dir(fpga4p.training_algorithms)),
                                filter(lambda x: x[-2:] == '_c', dir(fpga4p.classification_algorithms)),
                                serial.tools.list_ports.comports()]
        self._doc_list = [lambda module: getattr(fpga4p.training_algorithms, module).__doc__,
                          lambda module: getattr(fpga4p.classification_algorithms, module).__doc__,
                          None]

    # ==================================================================================================================

    def print_information(self):
        for i in range(len(self._name_list)):
            print(f'\n{GREEN}{UNDERLINE_ON}{self._name_list[i]}{UNDERLINE_OFF}:{RESET} ')
            for something in self._iterators_list[i]:
                    print(f'\n{UNDERLINE_ON}{self._type_list[i]}{UNDERLINE_OFF}: \t"{something}"')
                    if self._doc_list[i] is not None:
                        print(f'\n{UNDERLINE_ON}MODULE DOCUMENTATION{UNDERLINE_OFF}:',
                              self._doc_list[i](something))
                    print(f'{UNDERLINE_ON} {UNDERLINE_OFF}' * len(self._name_list[i]))

    # ==================================================================================================================


########################################################################################################################
# E N D   O F   F I L E .  #############################################################################################
########################################################################################################################
