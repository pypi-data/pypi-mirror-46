.. image:: https://bytebucket.org/tt-lab/ttlab/raw/07af7e037611c6d2b47aef425bc7e078519c04ce/assets/header.png?token=9425964a76732a6a54d81fb58935ae6dc8acbfa4

TT - lab
========

Easy to use import scripts for the most common physics equipments such as XPS, mass spectrometer, light spectrometers.
Functions for the most typical analysis procedures.

Installation
--------------
.. code-block:: console

    $ pip install ttlab


How to use
----------
For full explanation, see the documentation at 'link'.

Example with mass spectrometer data:

.. code-block:: python

    from ttlab import MassSpectrometer


    # Create a mass spec object
    filename = 'path/filename.asc'
    MS = MassSpectrometer(filename)

    # Check what gases are included in the data
    print(MS.gases)

    # Plot one of the gases, using matploltlib, returns the axes
    ax = MS.plot_gas('Ar')
    
    # Get the ion current and the relative time for the gas, returns np arrays with the data
    ion_current_argon = MS.get_ion_current('Ar')
    time_relative = MS.get_relative_time('Ar')

Want to contribute?
-------------------
With code?
Contact us at info.ttlab@gmail.com

License
-------
MIT license
Feel free to use ttlab in whatever way you want to.

