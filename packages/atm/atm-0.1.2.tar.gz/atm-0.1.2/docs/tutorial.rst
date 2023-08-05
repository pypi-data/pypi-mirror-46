Tutorial
========

Creating a Dataset
------------------
A Dataset in ATM is defined by the following fields:

Data format
^^^^^^^^^^^

ATM works with data in CSV format. For ATM to interpret it, each CSV file needs
the following

* Have the first line of the file be headers with strings as the feature names, and the class column named "class" (or configured otherwise in run_config.yaml). If the features aren't named (ie, image or SVD or PCA data), then anything will do (but see below for a small script to generate nice feature names).
* Should have N + 1 rows (1 header + N examples)
* Should have D + 1 features (1 class label + D features per example)

Here's a handy Python script to create a CSV header line for data that doesn't have feature names::


    def create_csv_header(n_features, name, class_label_name):
        """
            Creates a CSV header like:
                "<class_label_name>, <name>1, <name>2, ..., <name><n_features>"

            Example:
                print CreateCSVHeader(64, "pixel", "class")
        """
        separator = ","
        zip([name for i in range(n_features)], range(1, n_features + 1, 1))
        header_row_string = separator.join(
            [x + str(y) for (x, y) in
            ])
        return separator.join([class_label_name, header_row_string])


Creating a Datarun in the ModelHub
----------------------------------

Once your data in the proper format, you can upload it to the ModelHub for processing.

Configuration File
^^^^^^^^^^^^^^^^^^

To run ATM, you must create a configuration file.

A configuration file template is included in ``config/atm.cnf.template`` (and shown below).
Since the configuration file contains passwords, it's best to rename it to ``atm.cnf`` so that it will be ignored by git.
This is especially true if you plan to make changes to ATM and upload them to the repository.
The git repository is setup to ignore all files in the ``config`` folder except ``atm.cnf.template``.

The name of the file must also be a environmental variable called ``ATM_CONFIG_FILE``.
For example if the configuration file is called ``atm.cnf`` in the ``config`` directory of the root atm directory, then an environmental variable would created with the command::

    (atm-env) $ export ATM_CONFIG_FILE=/path_to_atm_root/config/atm.cnf

Datarun Creation
^^^^^^^^^^^^^^^^

Now we need to add the `datarun` to the ModelHub (database).
A datarun consists of all the parameters for a single experiment run, including where the find the data, what the budget is for number of learners to train, the majoirty class benchmark, and other things.
The datarun ID in the database also ties together the `hyperpartitions` (frozen sets) which delineate how ATM can explore different subtypes of classifiers to maximize their performance.
Once the configuration file is filled out, we can enter it in ModelHub with::

    (atm-env) $ atm enter_data

Workers
-------

Once at least one datarun is in the ModelHub, workers can be started to run classification routines.

On a Local Machine
^^^^^^^^^^^^^^^^^^

In local mode, this is simple::

    (atm-env) $ atm worker

This command can b executed several times to create many workers that operate independently in parallel.
How many to run depends of your judgment of your computer's capabilities.

On Amazon Web Services
^^^^^^^^^^^^^^^^^^^^^^
In cloud mode, the `fabric <https://www.fabfile.org>`_ package is used to deploy workers on AWS.
First, you must create instance(s) by executing the following command on your local machine::

    (atm-env) $ fab create_instances

The number of instances will be the number specified in the *aws* section of the configuration file.
Second, you must start ATM worker processes on the instance(s) by executing the following command on your local machine::

    (atm-env) $ fab deploy

The number of worker processes on each EC2 instance is specified in the configuration file.
Once the workers are done, the worker processes can be killed by executing the following command on your local machine::

    (atm-env) $ fab killworkers

**This does NOT terminate the instances**.
Currently, the instances have to be terminated from the AWS Management Console.
