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

    To `get started with Red Cloud <https://portal.cac.cornell.edu/techdocs/redcloud/#getting-started-on-red-cloud>`_,
    you will need to:

      * Go to the `CAC portal <https://portal.cac.cornell.edu/>`_ and log in.
        The instructions to log in are on the
        `CAC TechDocs page: Portal Login <https://portal.cac.cornell.edu/techdocs/general/CACportal/#portal-login>`_.

      * Get a CAC account by doing **one of** the following:

        1. Start a new project (only available for Cornell Faculty and Staff).
        2. Join an existing project.
        3. Request an exploratory account.

      * Once you join a project with Red Cloud subscription, log in to `Red Cloud Horizon web interface <https://redcloud2.cac.cornell.edu/>`_.

   The sections below will guide you through this process.
   For an overview of Red Cloud, read Cornell TechDocs `Red Cloud documentation <https://portal.cac.cornell.edu/techdocs/redcloud/>`_.

  .. dropdown:: Option 1: Start a Project

    One way to get a CAC account is to request a project. 
    Note that you must be a Cornell faculty member or staff member to view the pages below and start a project. 
    You may submit a project request at the CAC portal.
    Thoroughly review the `rates <https://portal.cac.cornell.edu/rates>`_ (login required) page to understand the Red Cloud subscription service.

    Once your project is approved, you can manage your project on the CAC portal.
    Read the `Portal Overview <https://portal.cac.cornell.edu/techdocs/general/CACportal/#portal-overview>`_ to learn
    how to manage a project.
    Detailed instructions to start a project are available at the `CAC TechDocs page: As a Cornell Faculty or Staff, How Do I Start a New Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#as-a-cornell-faculty-or-staff-how-do-i-start-a-new-project>`_

  .. dropdown:: Option 2: Join a Project

    To join an existing project, submit a request to join on the CAC portal.
    You should only do this if your PI has requested you to submit the request.
    Once the PI of the project approves the request,
    an email is sent to you with the login information.
    For the full instructions, navigate to the
    `CAC TechDocs page: How Do I Join an Existing Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#how-do-i-join-an-existing-project>`_.

  .. dropdown:: Option 3: Open an Exploratory Account

    You may also request an exploratory account if you have not made one already.
    This account has limited computing hours and storage. This is sufficient for the Hurricane Matthew exercise,
    but does not have enough compute hours to complete the LULC exercise.
    To request an exploratory account, follow the instructions on the
    `CAC TechDocs page: How Do I Request an Exploratory Project? <https://portal.cac.cornell.edu/techdocs/general/CACportal/#how-do-i-request-an-exploratory-project>`_ .
    You are also given one hour of free consulting for any help you may need.

  .. dropdown:: Log in to Red Cloud Horizon Interface

    Once you join a project with Red Cloud subscription, 
    you can log into the `Red Cloud Horizon web interface <https://redcloud2.cac.cornell.edu/>`_ .

  .. dropdown:: Create a Cloud Instance and Log In

    After you have logged in to the Red Cloud Horizon interface,
    you are ready to create the cloud instance where you will run the I-WRF simulation.
    If you are not familiar with the cloud computing terms "image" and "instance",
    it is recommended that you read about them here before proceeding:
    `Red Cloud: Images <https://portal.cac.cornell.edu/techdocs/redcloud/compute/#images>`_
    and `Red Cloud: Run Linux Instance <https://portal.cac.cornell.edu/techdocs/redcloud/run_linux_instances/>`_.

  .. dropdown:: Create an SSH Key

    You can either upload a public SSH key to Red Cloud or generate an SSH key pair on Red Cloud before creating your instance.
    Red Cloud injects the uploaded public key or generated public key into the instance's default user account,
    and you will need to provide the matching private SSH key to log in to the instance.
    If you are not familiar with "SSH key pairs", you should
    `read about them <https://portal.cac.cornell.edu/techdocs/redcloud/compute/#keypairs>`_ before continuing.

      * It's highly recommended that you
        `create a key pair on Red Cloud <https://portal.cac.cornell.edu/techdocs/redcloud/horizon_ssh_keys/#create-a-new-ssh-key-pair>`_.
        Be sure to follow the steps and save the private key it generated with the
        correct format and permission before proceeding.
        This is the easiest way to generate a key pair for this exercise.

      * Alternatively, `create an SSH Key on your computer <https://portal.cac.cornell.edu/techdocs/clusterinfo/linuxconnect/#public-key-authentication>`_
        using the "ssh-keygen" command.
        That command allows you to specify the name of the private key file it creates,
        with the default being "id_rsa".
        The matching public key file is saved and named with ".pub" appended to the filename.
        Then, `import the public key to Red Cloud <https://portal.cac.cornell.edu/techdocs/redcloud/horizon_ssh_keys/#import-a-public-key>`_ through the Red Cloud web interface.

  .. dropdown:: Create a Security Group

    Security groups are firewalls that control inbound and outbound network traffic to your instances.
    For an instance to be accessible, its security group must have port 22 (SSH) enabled.
    You can read more about them at `Red Cloud: Security Groups <https://portal.cac.cornell.edu/techdocs/redcloud/network/#security>`__.

    If you will access the instance from a Cornell Network (eduroam Wi-Fi, Ethernet, Cornell VPN, etc.),
    it's sufficient to use the security group that already exists on your project: "campus-only-ssh".
    This security group is already configured to enable SSH traffic from anywhere in the Cornell Network.

    If you cannot use any of the options above,
    you will need to create a security group and add an SSH rule for an IP address you frequently use.
    Follow the steps below to create a security group:

      * `Create a security group <https://portal.cac.cornell.edu/techdocs/redcloud/horizon_security_groups/#create-a-security-group>`__

      * `Add an SSH rule to the security group to allow SSH <https://portal.cac.cornell.edu/techdocs/redcloud/horizon_security_groups/#manage-your-security-group>`__

        * In the Rule dropdown, select "SSH"
        * In the CIDR field, put your IP address followed by "/32", e.g., "128.84.0.0/32"

    Note that once you put your IP address in the CIDR field, you may connect to the instance from that IP address.
    If your IP address changes for any reason, you will need to remove and update the rule.


  .. dropdown:: Create an Instance

    The Cornell TechDocs `Creating a New Linux Instance <https://portal.cac.cornell.edu/techdocs/redcloud/run_linux_instances/#creating-a-new-linux-instance>`_
    provides detailed information about creating a Linux instance on Red Cloud.
    While following those steps, be sure to make the following choices for this instance:

      .. dropdown:: Hurricane Matthew
        
        * When choosing an image as the instance source:
            
          * Select Boot from Source is "Image"
          * Volume Size (GB) is 100
          * Delete Volume on Instance Delete is "Yes"
          * Select the "ubuntu-24.04-LTS" image

        * In Flavor, choose the "Flavor" c4.m32 (4 Virtual CPUs) to provide a faster simulation run-time.
        * In Network, select "public".
        * In Security Groups, select "campus-only-ssh" or the security group you created.
        * In Key Pair, select the SSH public key that you created or uploaded previously.
          
      .. dropdown:: Land Use/Land Cover Change

        * When choosing an image as the instance source:
      
          * Select Boot from Source is "Image"
          * Volume Size (GB) is 1000
          * Delete Volume on Instance Delete is "Yes"
          * Select the "ubuntu-24.04-LTS" image

        * In Flavor, choose the "Flavor" c64.m120 (64 Virtual CPUs) to provide a faster simulation run-time. Note that this will consume Red Cloud subscriptions very fast.
        * In Network, select "public".
        * In Security Groups, select "campus-only-ssh" or the security group you created.
        * In Key Pair, select the SSH public key that you created or uploaded previously.

    When all the required options are selected, click on the "Launch Instance" button,
    and wait for the instance to enter the "Active" state.
    Note that the instance will not only be created,
    but will be running so that you can log in right away.

  .. dropdown:: Log in to the Instance

    The instructions for `connecting to Red Cloud Linux instances using SSH <https://portal.cac.cornell.edu/techdocs/redcloud/run_linux_instances/#accessing-instances>`_
    can be executed in the Command Prompt on Windows
    (from the Start menu, type "cmd" and select Command Prompt or search for PowerShell)
    or from the Terminal application on a Mac.

    In either case, you will need to know the location and name of the private SSH key
    created on your computer or downloaded from Red Cloud (see above),
    the IP address of your instance (found in the Red Cloud OpenStack interface)
    and the default username on your instance, which is "ubuntu".

    You will know that your login has been successful when the prompt has the form ``ubuntu@instance-name:~$``,
    which indicates your username, the instance name, and your current working directory, followed by "$"

  .. _manage-red-cloud-instance:

  .. dropdown:: Managing a Red Cloud Instance

    In order to use cloud computing resources efficiently, you must know how to
    `manage your Red Cloud instances <https://portal.cac.cornell.edu/techdocs/redcloud/compute/#instance-states>`_.
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
    Decreasing the number of CPUs may slow down your computations,
    but it will also reduce the cost per hour to run the instance.
    Increasing the number of CPUs can make your computations finish more quickly.
    Doubling the number of CPUs doubles the cost per hour to run the instance.
    Nonetheless, it's important to shelve the instance as soon as you are done.
    