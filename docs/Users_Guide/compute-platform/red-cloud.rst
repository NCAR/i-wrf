.. _compute-platform-red-cloud:

Red Cloud
---------

The `Red Cloud cloud computing platform <https://www.cac.cornell.edu/services/cloudservices.aspx/>`_,
provided by Cornell Center for Advanced Computing (CAC), is a subscription-based
Infrastructure as a Service cloud that provides root access to virtual servers and
on-demand storage to Cornell researchers.

It is recommended that you follow the instructions in each section in the order
presented to avoid encountering issues during the process. Most sections refer to
external documentation to provide details about the necessary steps and to offer
additional background information.

.. dropdown:: Instructions

  .. dropdown:: Prepare to Use Red Cloud

    To `get started with Red Cloud <https://www.cac.cornell.edu/services/projects.aspx>`_,
    you will need to:

      * Get a CAC account by doing **one of** the following:

        1. Start a new project by making a `project request <https://www.cac.cornell.edu/services/projects/project.aspx>`_ (Only available for Cornell Faculty and Staff).
        2. Join an existing project by `request to be added to a project <https://www.cac.cornell.edu/services/external/RequestCACid.aspx>`_.
        3. Request an exploratory account by `submitting a request <https://www.cac.cornell.edu/cu/explore.aspx>`_.

      * Log in to Red Cloud's OpenStack interface.

   The sections below will guide you through this process.
   For an overview of Red Cloud, read Cornell TechDocs `Red Cloud documentation <https://www.cac.cornell.edu/techdocs/redcloud/#red-cloud>`_.

  .. dropdown:: Option 1: Start a Project

    One way to create a CAC account is to request a project.
    Note that you must be a Cornell faculty member or a staff member to view the pages below and start a project.
    You may submit a `project request <https://www.cac.cornell.edu/services/projects/project.aspx>`_ at the CAC website.
    Thoroughly review the `rates <https://www.cac.cornell.edu/services/projects/rates.aspx>`_ page to understand the Red Cloud subscription service.

    Once your project is approved, you can `manage your project <https://www.cac.cornell.edu/services/projects/manage.aspx>`_, and
    read `this page <https://www.cac.cornell.edu/services/projects/project.aspx>`_ to learn how to manage a project.

  .. dropdown:: Option 2: Join a Project

    To join an existing project, submit a `join request <https://www.cac.cornell.edu/services/external/RequestCACid.aspx>`_.
    You should only do this if your PI has requested you to submit the request.
    Once the PI of the project approves the request, an email is sent to you with the login information.

  .. dropdown:: Option 3: Open an Exploratory Account

    You may also request an exploratory account if you have not made one already.
    This account has limited computing hours and storage but is sufficient for this exercise.
    To request an exploratory account, submit a `request <https://www.cac.cornell.edu/cu/explore.aspx>`_.
    You are also given one hour of free consulting for any help you may need.

  .. dropdown:: Log in to Red Cloud OpenStack Interface

    Once you are given a CAC account login information,
    you can log into the `Red Cloud OpenStack web interface <https://redcloud.cac.cornell.edu/>`_.
    Note that you need to be on a project with a subscription to log in successfully.

  .. dropdown:: Create a Cloud Instance and Log In

    After you have logged in to the Red Cloud OpenStack interface,
    you are ready to create the cloud instance where you will run the I-WRF simulation.
    If you are not familiar with the cloud computing terms "image" and "instance",
    it is recommended that you read about them `here <https://www.cac.cornell.edu/techdocs/openstack/images/>`__
    and `here <https://www.cac.cornell.edu/techdocs/redcloud/Red_Cloud_Linux_Instances/>`__ before proceeding.

  .. dropdown:: Create an SSH Key

    You can either upload a public SSH key to Red Cloud or generate an SSH key pair on Red Cloud before creating your instance.
    Red Cloud injects the uploaded public key or generated public key into the instance's default user account,
    and you will need to provide the matching private SSH key to log in to the instance.
    If you are not familiar with "SSH key pairs", you should
    `read about them <https://www.cac.cornell.edu/techdocs/openstack/keypairs/>`__ before continuing.

      * First, `create a Red Cloud SSH Key on your computer <https://www.cac.cornell.edu/techdocs/openstack/keypairs/#creating-a-passphrase-protected-key-pair-recommended>`_ using the "ssh-keygen" command.  That command allows you to specify the name of the private key file it creates, with the default being "id_rsa".  The matching public key file is saved and named with ".pub" appended to the filename.
      * Then, `import the public key to Red Cloud <https://www.cac.cornell.edu/techdocs/openstack/keypairs/#importing-a-key-pair>`_ through the Red Cloud web interface.

    Alternatively, you can `create a key pair on Red Cloud <https://www.cac.cornell.edu/techdocs/openstack/keypairs/#creating-a-key-pair-without-a-passphrase>`_. Be sure to follow the steps and save the private key it generated with the correct format and permission before proceeding.

  .. dropdown:: Create an Instance

    The Cornell TechDocs `Creating a New Linux Instance <https://www.cac.cornell.edu/techdocs/redcloud/Red_Cloud_Linux_Instances/#creating-a-new-linux-instance>`_
    provides detailed information about creating a Linux instance on Red Cloud.
    While following those steps, be sure to make the following choices for this instance:

      * When choosing an image as the instance source:
  
        * Select Boot from Source is "Image"
        * Volume Size (GB) is 100
        * Delete Volume on Instance Delete is "Yes"
        * Select the "ubuntu-22.04-LTS" image

     * In Flavor, choose the "Flavor" c4.m32 (4 Virtual CPUs) to provide a faster simulation run-time.
     * In Network, select "public".
     * In Key Pair, select the SSH public key that you uploaded previously.

    When all the required options are selected, click on the "Launch Instance" button, and wait for the instance to enter the "Active" state.
    Note that the instance will not only be created, but will be running so that you can log in right away.

  .. dropdown:: Log in to the Instance

    The instructions for `connecting to Red Cloud Linux instances using SSH <https://www.cac.cornell.edu/techdocs/redcloud/Red_Cloud_Linux_Instances/#accessing-instances>`_
    can be executed in the Command Prompt on Windows (from the Start menu, type "cmd" and select Command Prompt)
    or from the Terminal application on a Mac.

    In either case, you will need to know the location and name of the private SSH key created on your computer (see above),
    the IP address of your instance (found in the Red Cloud OpenStack interface)
    and the default username on your instance, which is "ubuntu".

    You will know that your login has been successful when the prompt has the form ``ubuntu@instance-name:~$``,
    which indicates your username, the instance name, and your current working directory, followed by "$"

  .. _manage-red-cloud-instance:

  .. dropdown:: Managing a Red Cloud Instance

    In order to use cloud computing resources efficiently, you must know how to
    `manage your Red Cloud instances <https://www.cac.cornell.edu/techdocs/openstack/#instance-states>`_.
    Instances incur costs whenever they are running (on Red Cloud, this is when they are "Active").
    "Shelving" an instance stops it from using the cloud's CPUs and memory,
    and therefore stops it from incurring any charges against your project.

    When you are finished running I-WRF,
    be sure to use the instance's dropdown menu in the web interface to
    "Shelve" the instance so that it is no longer spending your computing hours.
    If you later return to the web interface and want to use the instance again,
    Use the dropdown menu's "Unshelve Instance" option to start the instance up again.
    Note that any programs that were running when you shelve the instance will be lost,
    but the contents of the disk are preserved when shelving.

    You may also want to try the "Resize" action to change the number of CPUs of the instance.
    Increasing the number of CPUs (say, to flavor "c8.m64") can make your computations finish more quickly.
    But of course, doubling the number of CPUs doubles the cost per hour to run the instance,
    so Shelving as soon as you are done becomes even more important!
