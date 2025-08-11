.. _compute-platform-jetstream2:

Jetstream2
----------

The `Jetstream2 cloud computing platform <https://jetstream-cloud.org/>`_
is a flexible, user-friendly cloud computing environment available to U.S.-based
researchers and educators at no cost through support from the National Science
Foundation's Advanced Cyberinfrastructure Coordination.

It is recommended that you follow the instructions in each section in the order
presented to avoid encountering issues during the process. Most sections refer to
external documentation to provide details about the necessary steps and to offer
additional background information.

.. dropdown:: Instructions

  .. dropdown:: Get an ACCESS Account
  
    To `get started with Jetstream2 <https://jetstream-cloud.org/get-started>`_,
    you will need to create an account with the `National Science Foundation (NSF) <https://www.nsf.gov/>`_'s
    `ACCESS program <https://access-ci.org/>`_. If you do not already have one,
    `register for an ACCESS account <https://operations.access-ci.org/identity/new-user>`_.
    When registering your account, you can either choose to associate your existing
    University/Organizational account or create an entirely new ACCESS account when registering.
    The Jetstream2 team strongly recommends that you create a new ACCESS account,
    as your organizational affiliation may change in the future.

  .. dropdown:: Add ACCESS Account Allocation

    Once you have an account you will need to have a computational "allocation" added to that account.
    Allocations provide the credits you will spend when running instances on Jetstream2.
    If there are no allocation owners who can add you to their allocation and you are interested in obtaining your own,
    you may `request an allocation <https://allocations.access-ci.org/get-your-first-project>`_
    that will allow you to use an ACCESS-affiliated cyberinfrastructure resource.
    Note that allocations may only be requested by faculty, staff and graduate researchers,
    so undergraduates must work with a faculty sponsor to requeste an allocation.

    Be sure to read all of the information on the request page so that you make a suitable request.
    Note that you will need to describe the project for which the allocation is intended
    and provide a CV or resume for the principal investigator.
    An "Explore" project (400,000 credits) will be much more than enough to work with this exercise.
    You will want to work with the resource "Indiana Jetstream2 CPU" (*not* **GPU**).
    The typical turnaround time for allocation requests is one business day.

  .. dropdown:: Log in to Jetstream2's Exosphere Web Site

    Once you have an ACCESS account and an allocation has been added to it,
    you can log in to Jetstream's `Exosphere web dashboard <https://jetstream2.exosphere.app>`_.
    The process of identifying your allocation and ACCESS ID to use Jetstream2
    is described on `this page <https://cvw.cac.cornell.edu/jetstream/intro/jetstream-login>`__ of the
    `Introduction to Jetstream2 <https://cvw.cac.cornell.edu/jetstream>`_ Cornell Virtual Workshop,
    and on `this page <https://docs.jetstream-cloud.org/ui/exo/login>`__
    of the `Jetstream2 documentation <https://docs.jetstream-cloud.org>`_.
    
    While adding an allocation to your account, it is recommended that you choose
    the "Indiana University" region of Jetstream2 for completing this exercise.

  .. dropdown:: Create a Cloud Instance on Jetstream2

    After you have logged in to Jetstream2 and added your allocation to your account,
    you are ready to create the cloud instance where you will run the simulation and verification.
    If you are not familiar with the cloud computing terms "image" and "instance",
    it is recommended that you `read about them <https://cvw.cac.cornell.edu/jetstream/intro/imagesandinstances>`__
    before proceeding.

    For this tutorial, you will be able to log in to your instance using Exosphere's Web Desktop or Web Shell functionalities.
    If you would rather log in using the :code:`ssh` command from a shell on your own computer,
    you will need to create an SSH key pair and upload it to Jetstream2 before creating your instance.
    Optional information about doing those things is available here:

      .. dropdown:: Creating an SSH Key and uploading it to Jetstream2 (Optional)

        You may choose to upload a public SSH key to Jetstream2 before creating your instance.
        Jetstream2 will inject that public key into an instance's default user account,
        and you will need to provide the matching private SSH key to log in to the instance.
        If you are not familiar with "SSH key pairs", you should
        `read about them <https://cvw.cac.cornell.edu/jetstream/keys/about-keys>`__ before continuing.

          * First, `create a Jetstream2 SSH Key on your computer <https://cvw.cac.cornell.edu/jetstream/keys/ssh-create>`_ using the :code:`ssh-keygen` command. That command allows you to specify the name and location of the private key file it creates, with the default being "id_rsa". The matching public key file is saved to the same location and name with :code:`.pub` appended to the filename. Later instructions will assume that your private key file is named :code:`id_rsa`, but you may choose a different name now and use that name in those later instructions.
          * Then, `upload the public key to Jetstream2 <https://cvw.cac.cornell.edu/jetstream/keys/ssh-upload>`_ through the Exosphere web interface.

    The Cornell Virtual Workshop topic `Creating an Instance <https://cvw.cac.cornell.edu/jetstream/create-instance>`_
    provides detailed information about creating a Jetstream2 instance.
    While following those steps for this tutorial, be sure to make the following choices for this instance:

      .. dropdown:: Hurricane Matthew
        
        * When choosing an image as the instance source, if viewing "By Type", select the "Ubuntu 22.04" image.  If viewing "By Image", choose the "Featured-Ubuntu22" image.
        * Choose the "Flavor" m3.quad (4 CPUs) to provide a faster simulation run-time.
        * Select a custom disk size of 100 GB, which is large enough to hold this exercise's data and results.
        * For "Enable web desktop?", select Yes.
        * For "Choose an SSH public key", select None unless you want to use your own SSH key that you uploaded previously.
        * You do not need to set any of the Advanced Options.

      .. dropdown:: Land Use/Land Cover Change
        
        * When choosing an image as the instance source, if viewing "By Type", select the "Ubuntu 24.04" image.  If viewing "By Image", choose the "Featured-Ubuntu24" image.
        * Choose the "Flavor" m3.2xl (64 CPUs) to provide a faster simulation run-time.
        * Select a custom disk size of 1000 GB, which is large enough to hold this exercise's data and results.
        * For "Enable web desktop?", select Yes.
        * For "Choose an SSH public key", select None unless you want to use your own SSH key that you uploaded previously.
        * You do not need to set any of the Advanced Options.

    After clicking the "Create" button, wait for the instance to enter the "Ready" state (it takes several minutes).
    Note that the instance will not only be created, but will be running so that you can log in right away.

  .. dropdown:: Log in to the Instance

    The Exosphere web dashboard provides two easy-to-use methods for logging in to your instance through a web browser.
    The "Web Shell" button will open a terminal to your instance,
    and the "Web Desktop" button will open a view of the instance's graphical desktop (if enabled).
    Both views open in a new browser tab, and Exosphere automatically logs you in to the instance.
    For this tutorial you should open a Web Desktop so that you will be able to view
    the plots that are generated from the simulation output.

    If you wish to log in to the instance from a shell on your computer,
    you can do so following the information in this optional content:

    .. dropdown:: Logging in to a Jetstream2 Instance using SSH From a Shell

      You can use the SSH command to access your instance from a shell on your computer.
      The instructions for `connecting to Jetstream2 using SSH <https://cvw.cac.cornell.edu/jetstream/instance-login/sshshell>`_
      can be executed in the Command Prompt on Windows (from the Start menu, type "cmd" and select Command Prompt)
      or from the Terminal application on a Mac.

    In either case you will need to know the location and name of the private SSH key created on your computer (see SSH section, above),
    the IP address of your instance (found in the Exosphere web dashboard)
    and the default username on your instance, which is "exouser".

    Once you are logged in to the instance, your shell prompt will have the form ``exouser@instance-name:~$``,
    which indicates your username, the instance name, and your current working directory, followed by "$".
    
    If your shell ever becomes unresponsive or disconnected from the instance,
    you can recover from that situation by opening a new Web Desktop (if available) or rebooting the instance.
    In the Exosphere dashboard page for your instance, in the Actions menu, select "Reboot".
    The process takes several minutes, after which the instance status will return to "Ready".

  .. _manage-jetstream2-instance:

  .. dropdown:: Managing a Jetstream2 Instance

    In order to use cloud computing resources efficiently, you must know how to
    `manage your Jetstream2 instances <https://cvw.cac.cornell.edu/jetstream/manage-instance/states-actions>`_.
    Instances incur costs whenever they are running (on Jetstream2, this is when they are "Ready").
    "Shelving" an instance stops it from using the cloud's CPUs and memory,
    and therefore stops it from incurring any charges against your allocation.

    When you are through working on an I-WRF exercise, you should shelve your instance.
    Note that any programs that are running when you shelve the instance will be terminated,
    but the contents of the disk are preserved when shelving.

    To shelve, you need to be in the details page for your instance (with the "Actions" menu in the upper right).
    If you are on the Instances page, click and instance's name to be taken to its details page.
    From the Actions menu, select Shelve.
    You will be prompted in that location to confirm the shelve action - click Yes to complete the action.
    In the Instances page your instance will briefly be listed as "Shelving",
    and then as "Shelved" when the operation is complete.

    When you later return to the dashboard and want to use the instance again,
    use the Action menu's "Unshelve" option to start the instance up again.
    You can also use the "Resize" action to change the flavor (number of CPUs and amount of RAM) of the instance.
    Increasing the number of CPUs can make your computations finish more quickly,
    but doubling the number of CPUs doubles the cost per hour to run the instance,
    so Shelving as soon as you are done becomes even more important!
