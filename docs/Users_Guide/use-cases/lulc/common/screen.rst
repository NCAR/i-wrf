
.. dropdown:: Using Screen in Linux

  This exercise has two options: simulate the Dallas-Fort Worth area over a
  3 hour period or over a 36 hour period.
  In either case, your simulation may run for several hours or for several days.
  During this time, any disconnects from the instance will interrupt the simulation.
  For this reason, it's almost necessary to use the Linux command ``screen``.
  By using ``screen``, you create and enter a screen session.
  Within it, you may run commands as if you were in a normal terminal.
  You can disconnect from the screen session or the instance,
  and any ongoing process will continue in the background.
  At any time, SSH back into the instance and connect to the
  screen session to check the progress.
  Disconnecting from and connecting to a screen session is called
  "detaching" and "attaching".
  In this exercise, we will only use part of the functionalities of ``screen``.
  You may see the full documentation of ``screen`` at
  `GNU Screen <https://www.gnu.org/software/screen/manual/screen.html>`_.

  To start a screen session with ``lulc`` as the session name,
  enter the following into your terminal::

      screen -S lulc

  To show all running screen sessions and see if you are attached to any screen sessions,
  enter the following
  (if you started a screen session, it displays that you are attached to one)::

      screen -ls

  Inside a screen session, if you want to detach from it,
  you would need to press a combination of keys::
    
      Ctrl+A, D

  To attach to the screen session ``lulc``, enter the following::

      screen -r lulc
