.. _lulc-jetstream2:

On Jetstream2
^^^^^^^^^^^^^

Follow the compute platform instructions for :ref:`compute-platform-jetstream2`
to secure access to and log in to Jetstream2.

.. dropdown:: Instructions

  .. dropdown:: Instance Configuration

    .. _jetstream2_instance_configuration:

    Make the following choices when creating your instance:
    
      * When choosing an image as the instance source, if viewing "By Type", select the "Ubuntu 24.04" image.  If viewing "By Image", choose the "Featured-Ubuntu24" image.
      * Choose the "Flavor" m3.2xl (64 CPUs) to provide a faster simulation run-time.
      * Select a custom disk size of 1000 GB, which is large enough to hold this exercise's data and results.
      * For "Enable web desktop?", select Yes.
      * For "Choose an SSH public key", select None unless you want to use your own SSH key that you uploaded previously.
      * You do not need to set any of the Advanced Options.

  .. include:: lulc/common/preparingenvironment.rst

  .. dropdown:: Recovering Unresponsive Instance

    If your shell ever becomes unresponsive or disconnected from the instance,
    you can recover from that situation by opening a new Web Desktop (if available) or rebooting the instance.
    In the Exosphere dashboard page for your instance, in the Actions menu, select "Reboot".
    The process takes several minutes, after which the instance status will return to "Ready".

  .. include:: lulc/common/getdockerimage.rst

  .. dropdown:: Install and Enable CephFS

    You need to access the data used in this exercise. In total, the full data are close to 90 GB in size. Usually, such large datasets cannot be shared easily. However, Jetstream2 has a Ceph cluster, a distributed file system that stores the data locally at Jetstream2. Any Linux machine on Jetstream2 can access this data using the following steps.

    First, update the package list::

        sudo apt update

    Install CephFS client::

        sudo apt install ceph-common

    The CephFS mounting steps are slightly more complicated. When a CephFS share is created, access rules must be set for writing or reading the data. This credential is called a keyring, which consists of an entity name (accessTo) and a key (accessKey). For this exercise, copy and paste the credentials for read-only access::

        accessTo="iwrf-lulc-read-only"
        accessKey="AQCLixNooPVSGBAASckRTu+xrJeDzaoQQEv6SQ=="

    The following commands set up the keyring::

        mkdir -p /etc/ceph
        echo -e "[client.${accessTo}]\n    key = ${accessKey}" | sudo tee /etc/ceph/ceph.client.${accessTo}.keyring

    The keyring file must be only readable to root::

        sudo chown root:root /etc/ceph/ceph.client.${accessTo}.keyring
        sudo chmod 600 /etc/ceph/ceph.client.${accessTo}.keyring

    Choose the mount point for the CephFS share, which will be in the home directory::

        cephfsPath="149.165.158.38:6789,149.165.158.22:6789,149.165.158.54:6789,149.165.158.70:6789,149.165.158.86:6789:/volumes/_nogroup/6e81fe46-b69e-4d33-be08-a2580b420b81/6cc28fc1-35f3-41b4-8652-f14555097810"
        mountPoint="/home/exouser/lulc_input"

    Mount to the location::

        echo "${cephfsPath} ${mountPoint} ceph name=${accessTo},x-systemd.device-timeout=30,x-systemd.mount-timeout=30,noatime,_netdev,rw 0 2" | sudo tee -a /etc/fstab
        sudo systemctl daemon-reload
        mkdir -p ${mountPoint}
        sudo mount ${mountPoint}

    Run the following command to test if mount is successful::

        df -h ${mountPoint}

    If the CephFS share is mounted correctly, the following output is shown:

    .. raw:: html

        <style>
            .no-copybutton .copybtn {
                display: none !important;
            }
        </style>

    .. code-block:: console
        :class: no-copybutton

        Filesystem                                                                                                                                                                                       Size  Used Avail Use% Mounted on
        149.165.158.38:6789,149.165.158.22:6789,149.165.158.54:6789,149.165.158.70:6789,149.165.158.86:6789:/volumes/_nogroup/6e81fe46-b69e-4d33-be08-a2580b420b81/6cc28fc1-35f3-41b4-8652-f14555097810  100G   85G   16G  85% /home/exouser/lulc_input

  .. include:: lulc/common/configfiles.rst

  .. include:: lulc/common/screen.rst

  .. include:: lulc/common/instructions.rst

  .. dropdown:: View Full WRF Output

    If you do not have the resources to run the entire simulation but would like to see the results, paste the following commands to access the full output Ceph share::

        accessTo="iwrf-lulc-output-read-only"
        accessKey="AQCv7EloaSlPERAAlXaru8qHfl6d+/3u+yx36g=="
        cephfsPath="149.165.158.38:6789,149.165.158.22:6789,149.165.158.54:6789,149.165.158.70:6789,149.165.158.86:6789:/volumes/_nogroup/83cfc802-c288-4727-991d-e33da52b36e4/4fd211a1-c611-4948-8444-bb4ec166b7a7"
        mountPoint="/home/exouser/lulc_full_output"

    ::

        mkdir -p /etc/ceph
        echo -e "[client.${accessTo}]\n    key = ${accessKey}" | sudo tee /etc/ceph/ceph.client.${accessTo}.keyring

    ::

        sudo chown root:root /etc/ceph/ceph.client.${accessTo}.keyring
        sudo chmod 600 /etc/ceph/ceph.client.${accessTo}.keyring

    ::

        echo "${cephfsPath} ${mountPoint} ceph name=${accessTo},x-systemd.device-timeout=30,x-systemd.mount-timeout=30,noatime,_netdev,rw 0 2" | sudo tee -a /etc/fstab

    ::

        sudo systemctl daemon-reload

    ::

        mkdir -p ${mountPoint}
        sudo mount ${mountPoint}

    ::

        df -h ${mountPoint}

    The full output should be in ``/home/exouser/lulc_full_output``.
