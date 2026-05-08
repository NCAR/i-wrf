.. _lulc-red-cloud:

On Red Cloud
^^^^^^^^^^^^

Follow the compute platform instructions for :ref:`compute-platform-red-cloud`
to secure access to and log in to Red Cloud.

.. dropdown:: Instructions

  .. dropdown:: Instance Configuration
    
    .. _redcloud_instance_configuration:

    Make the following choices when creating your instance:

      * When choosing an image as the instance source:
      
        * Select Boot from Source is "Image"
        * Volume Size (GB) is 1000
        * Delete Volume on Instance Delete is "Yes"
        * Select the "ubuntu-24.04-LTS" image

      * In Flavor, choose the "Flavor" c64.m120 (64 Virtual CPUs) to provide a faster simulation run-time. Note that this will consume Red Cloud subscriptions very fast.
      * In Network, select "public".
      * In Security Groups, select "campus-only-ssh" or the security group you created.
      * In Key Pair, select the SSH public key that you created or uploaded previously.

  .. include:: lulc/common/preparingenvironment.rst

  .. include:: lulc/common/getdockerimage.rst

  .. dropdown:: Install and Enable CephFS

    You need to access the data used in this exercise.
    In total, the full data are close to 90 GB in size.
    Usually, such large datasets cannot be shared easily.
    However, Red Cloud now has a Ceph cluster,
    a distributed file system that stores the data locally at Cornell CAC.
    Any Linux machine on the Cornell network can access this data using the following steps.

    First, update the package list::

        sudo apt update

    Install CephFS client::

        sudo apt install ceph-common

    The CephFS mounting steps are slightly more complicated. When a CephFS share is created, access rules must be set for writing or reading the data. This credential is called a keyring, which consists of an entity name (accessTo) and a key (accessKey). For this exercise, copy and paste the credentials for read-only access::

        accessTo="iwrf-lulc-read-only"
        accessKey="AQBsg0lozVQiDxAAZYNFvpyD9lqdzYD1ouv/Wg=="

    The following commands set up the keyring::

        mkdir -p /etc/ceph
        echo -e "[client.${accessTo}]\n    key = ${accessKey}" | sudo tee /etc/ceph/ceph.client.${accessTo}.keyring

    The keyring file must be only readable to root::

        sudo chown root:root /etc/ceph/ceph.client.${accessTo}.keyring
        sudo chmod 600 /etc/ceph/ceph.client.${accessTo}.keyring

    Choose the mount point for the CephFS share, which will be in the home directory::

        cephfsPath="128.84.20.11:6789,128.84.20.12:6789,128.84.20.15:6789,128.84.20.13:6789,128.84.20.14:6789:/volumes/_nogroup/e91d7ccd-9845-4d2a-acc6-d40e572ee796/937df611-6035-47bc-92ed-ad09fb225715"
        mountPoint="/home/ubuntu/lulc_input"

    Mount to the location::

        echo "${cephfsPath} ${mountPoint} ceph name=${accessTo},x-systemd.device-timeout=30,x-systemd.mount-timeout=30,noatime,_netdev,rw 0 2" | sudo tee -a /etc/fstab
        sudo systemctl daemon-reload
        mkdir -p ${mountPoint}
        sudo mount ${mountPoint}

    You might encounter some errors during the mount step.
    Disregard these errors, and run the following command to test if mount is successful::

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

        Filesystem                                                                                                                                                                             Size  Used Avail Use% Mounted on
        128.84.20.11:6789,128.84.20.12:6789,128.84.20.15:6789,128.84.20.13:6789,128.84.20.14:6789:/volumes/_nogroup/e91d7ccd-9845-4d2a-acc6-d40e572ee796/937df611-6035-47bc-92ed-ad09fb225715  100G   85G   16G  85% /home/ubuntu/lulc_input

  .. include:: lulc/common/configfiles.rst

  .. include:: lulc/common/screen.rst

  .. include:: lulc/common/instructions.rst

  .. dropdown:: View Full WRF Output

    If you do not have the resource to run the entire simulation but would like to see the results, paste the following commands to access the full output Ceph share::

        accessTo="iwrf-lulc-output-read-only"
        accessKey="AQCe60lo0kUiJBAAkf9bYacxnfjVM4zcku67Xw=="
        cephfsPath="128.84.20.11:6789,128.84.20.12:6789,128.84.20.15:6789,128.84.20.13:6789,128.84.20.14:6789:/volumes/_nogroup/4686628e-540f-4e99-8cd1-9e53dcb9f97d/686fafb3-94a2-4547-b33a-178f1f59ff8f"
        mountPoint="/home/ubuntu/lulc_full_output"

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

    The full output should be in ``/home/ubuntu/lulc_full_output``.
