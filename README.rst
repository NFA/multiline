=================================
 multiline
=================================

Overview
========
This module provides a simple interface for communicating to a WTW_® MultiLine
portable meter. It uses pySerial_ to communicate over the serial connection. This
module was created using a MultiLineIDS 3630 device for testing, however it is 
likely that it will work with the other MultiLineIDS devices as well as the inoLab
devices.

- Project Homepage: https://github.com/NFA/multiline


WTW_® is a brand in the Xylem_ group, and I, the author of this script have
no affiliation with either. I am just a researcher attempting to make my life
in the lab easier.


MIT License Copyright (c) 2020 Fredrik Nyström <nfa106@gmail.com>

Usage
=============
You will need some way of emulating a serial-usb connection. On Windows the 
easiest way is to install the virtual device driver supplied with the instrument, 
or from their downloads section on the respective product page.

.. highlight:: python
.. code-block:: python

   from multiline import MultiLineIDS

   def measurement(raw, parsed)
       print(raw) # raw string, unprocessed csv string from read_instrument
       print(parsed) # dict, parsed out all information
       ...

   dev = MultiLineIDS(port = <port>, callback = measurement)
   dev.read_instrument()


.. _WTW: https://www.wtw.com/en/
.. _pySerial: https://pythonhosted.org/pyserial/
.. _Xylem: https://www.xylem.com/ 
