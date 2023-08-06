########################################################################################################################
# M O D U L E   D O C U M E N T A T I O N : ############################################################################
########################################################################################################################


"""
The entry point of "fpga4p".

This module contains the entry point of the application. Depending on the arguments passed,
 launches the core or displays an informational message. Contains a message,
 that appears when the --help parameter is passed.

Example:
    This example starts the training task:

        $ python3 start.py -t "training.csv,train_nbc"

    This example starts the classification task:

        $ python3 start.py -c "classification.csv,classify_nbc,training.wd,/dev/ttyUSB0"

    This example prints available modules for training and classification,
     as well as available serial USB ports:

        $ python3 start.py -i

    For more information about the format of the arguments, use the parameter "--help".

Functions:
    launch: The entry point of the application.
"""


########################################################################################################################
# I M P O R T :  #######################################################################################################
########################################################################################################################


import click
import fpga4p
import os
from fpga4p.supporting_tools.special_characters import *
from fpga4p.supporting_tools.notifications import InformationTemplate


########################################################################################################################
# E N T R Y   P O I N T :  #############################################################################################
########################################################################################################################

# ======================================================================================================================

# Declaration of the entry point for terminal call: --------------------------------------------------------------------
@click.command()
# ----------------------------------------------------------------------------------------------------------------------
# Declaration of the parameters for terminal call: ---------------------------------------------------------------------
@click.option('-t', default=None,
              help=(f'{UNDERLINE_ON}t{UNDERLINE_OFF}rain ["training_file_1.csv,training_algorithm_1;...;'
                    'training_file_N.csv,training_algorithm_N"]'))
@click.option('-c', default=None,
              help=(f'{UNDERLINE_ON}c{UNDERLINE_OFF}lassify'
                    ' ["classification_file_1.csv,classification_algorithm_1,word_dict_1.wd,serial_port_1;...;'
                    'classification_file_N.csv,classification_algorithm_N,word_dict_N.wd,serial_port_N"]'))
@click.option('-v', is_flag=True,
              help=f'{UNDERLINE_ON}V{UNDERLINE_OFF}erbose mode.')
@click.option('-i', is_flag=True,
              help=f'Print {UNDERLINE_ON}i{UNDERLINE_OFF}nformation about'
                   ' available algorithms for training and classification and'
                   ' available serial USB ports.')
@click.option('-s', is_flag=True,
              help=f'{UNDERLINE_ON}S{UNDERLINE_OFF}plit training.csv for 2 samples 30%:70%.')
@click.option('-a', is_flag=True,
              help=f'Count {UNDERLINE_ON}a{UNDERLINE_OFF}ccuracy.')
def launch(t: str, c: str, v: bool, i: bool, s: bool, a: bool):
    # Output for "--help" option: --------------------------------------------------------------------------------------
    """
    MANUAL:

    "-t" (training) parameter:
        Accepts a string with arguments for training the model.

        Training tasks executes in parallel processes. Each training task
         generates: ".sv" file for FPGA, ".wd" file and ".tar" archive
         with model data for prospective classification task.

        Training rules:
            1) "training_file.csv" must contain classes in the first column.

            2) "training_file.csv" must not contain a column head.

            3) The character - separator of "training_file.csv" must be ",".

            4) You can check available training algorithms with option "--info".

    "-c" (classification) parameter:
        Accepts a string with arguments for classification the passed data set.

        Classification tasks might be executed parallel on several FPGAs.
         Several classification tasks, addressed to FPGA, execute consistently.
         Each classification task generates ".csv" file with predicted answers.

        Classification rules:
            1) "classification_file.csv" must not contain a column head.

            2) The character - separator of "training_file.csv" must be ",".

            3) The "word_dict.wd" might match to firmware of FPGA.

            4) You can check available training algorithms and USB serial ports
                with option "--info".

    "-s" (split) flag:
        In case the "-t" parameter is passed, it breaks the file into a training
         and test sample in the ratio of 70/30.

    "-v" (verbose) flag:
        Enables verbose output of all errors.

        All additional notifications are highlighted in yellow.

    "-i" (information) flag:
        Displays a message about the available algorithms and serial ports.

    "-a" (accuracy) flag:
        Calculates classification accuracy.

        The sample passed for classification must contain the classes
         in the first column.

    Examples:

         1) This example starts the training task:

            $ fpga4p -t "training.csv,nbc_t"

        2) This example starts the classification task:

            $ fpga4p -c "class.csv,nbc_c,training.wd,/dev/ttyUSB0"

        3) This example prints available modules for training and
            classification, as well as available serial USB ports:

            $ fpga4p -i

    """
    # ------------------------------------------------------------------------------------------------------------------

    # If "-i" flag was given: --------------------------------------------------------------------------------------
    if i:
        information = InformationTemplate()
        information.print_information()
        return 0
    # ------------------------------------------------------------------------------------------------------------------

    # If "-i" flag was not given: --------------------------------------------------------------------------------------
    else:
        if c is not None:
            # Print notification about ROOT rights: --------------------------------------------------------------------
            print(f'\n{UNDERLINE_ON}FPGA4P needs ROOT rights for communication with serial ports:{UNDERLINE_OFF}\n')
            # ----------------------------------------------------------------------------------------------------------

            # Request ROOT rights in the terminal: ---------------------------------------------------------------------
            fail = os.system('sudo echo')
            if not fail:
                print(f'\n{GREEN}{UNDERLINE_ON}ROOT rights obtained!{RESET}')
            else:
                print(f'\n{RED}{UNDERLINE_ON}ROOT rights did not obtain!{RESET}')
                print(f'\n{RED}Classification tasks will be not executed!{RESET}')
                c = None
            # ----------------------------------------------------------------------------------------------------------

        # Start the core module: ---------------------------------------------------------------------------------------
        core = fpga4p.core.Core(t=t, c=c, v=v, s=s, a=a)
        core.start()

        # --------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

# ======================================================================================================================


if __name__ == '__main__':
    launch()

# ======================================================================================================================

########################################################################################################################
# E N D   O F   F I L E .  #############################################################################################
########################################################################################################################
