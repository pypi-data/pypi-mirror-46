======================================
Chameleon Experiment Precis Client
======================================

Users can use this command line tool to generate a "history" of openration events performed on Chameleon Testbed corresponding to a user session in json format.
An experiment precis is defined as a series of real-time events a user performed under a lease of a project. Corresponding hardware and metric information is also included. 

_______________
Install
_______________

   .. code-block:: shell
   
      pip install cepclient

_______________
Run
_______________

Before requesting the experiment precis using CEP client, user needs to provide Chameleon authentication information. 
You can either ``source`` `the OpenStack RC file <https://chameleoncloud.readthedocs.io/en/latest/technical/cli.html#the-openstack-rc-script>`_
or pass the authentication information as command line arguments. 
Use ``cep --help`` for authentication options and usage details. 

To list all experiment precis, use command:

   .. code-block:: shell
      
      cep list

      # use help for more information
      cep list --help

To get an experiment precis, use command:

   .. code-block::shell
   
      cep print <ep name or id>

      # use help for more information
      cep print --help

You can apply different filters to print experiment precis. For example, use ``--exclude-hardware`` to hide hardware information 
or use ``--exclude-metric`` to screen out metrics from the printed experiment precis. 
In addition, you can prettyprint the experiment precis by passing ``--pretty`` argument. 
To save the experiment precis to a file, specify output location using ``--output`` argument. 
For more options of printing an experiment precis, use ``cep print --help``.

To rename an experiment precis, use command:

   .. code-block:: shell
   
      cep rename --name <new name> <ep name or id>

      # use help for more information
      cep rename --help