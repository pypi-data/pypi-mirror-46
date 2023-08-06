
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



