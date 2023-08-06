.. _usage:

=====
Usage
=====

After installing the plugin (please see :ref:`installation`),
a new *Test protocol IO* button will appear in each of the
already configured Setups.

.. warning::
    At the moment, it is required that a Bpod device is connected to the computer to run the module.

.. note::
    The button will only be *active* when there is both a valid board and protocol selected in the Setup details.

When pressing the button, with a Bpod device connected, the window presented in the next figure will appear.

.. figure:: _static/emulator_mainwindow.png
   :align: center
   :alt: PyBpod's Main window with the Emulator Window opened

   PyBpod's Main window with the Emulator Window opened

At the top of the window it is possible to see the selected Setup, the selected Board and protocol. The buttons that
are also available in the Setup details of PyBpod are also available in the Emulator window (i.e., Run, Stop trial and
Pause).

Afterwards, a section with the Behaviour Ports is presented with three rows of buttons, each button for each available
port. Each row represents the Valve, LED and the Poke.

.. note::
    The Emulator window will **adapt automatically** depending on the Bpod device version connected. For example, when
    connecting a Bpod v0.7, each row for the Behaviour Ports will present 8 buttons, representing the 8 Behaviour
    Ports available in that model.

After the Behaviour Ports, a section with the BNC connections is displayed, with two buttons for the inputs and two for
the outputs.

For Bpod v0.7 a new section with the Wire connections will appear after the BNC connections as it is possible to see in
the next figure.

.. figure:: _static/emulator_bpod07.png
   :align: center
   :alt: Emulator Window for Bpod v0.7

   Emulator Window for Bpod v0.7

When modules are connected to Bpod, they will also show up at the bottom of the window so it will be possible to send
serial messages to those modules using the Emulator.

Interaction
===========

To use the Emulator it is required, at the moment, that a device is connected and that a protocol is running. As such,
the first step is to run the protocol using the appropriate button.

While the protocol is running, when pressing the different buttons for different actions, different events will be
triggered.

As an example, if the Poke button 1 is pressed once (active state), it will trigger the 'Port1In' event.
If pressed again (disabled state), it will trigger the 'Port1Out' event. As such, when running the example protocol
presented below, which changes state when the 'Port1Out' event occurs, the PWM1 output channel (LED) will be turned on
during the 3 seconds duration of the state 'Port3LightOn'. When pressing the Poke button 1 twice, both the 'Port1In' and
'Port1Out' events are triggered by Bpod as if there was a real interaction in the Poke of the Behaviour Port.

.. code-block:: python

    from pybpodapi.protocol import Bpod, StateMachine

    my_bpod = Bpod()

    sma = StateMachine(my_bpod)

    sma.add_state(
        state_name='Port1LightOn',
        state_timer=1,
        state_change_conditions={Bpod.Events.Port1Out: 'Port3LightOn'},
        output_actions=[])

    sma.add_state(
        state_name='Port3LightOn',
        state_timer=3,
        state_change_conditions={Bpod.Events.Tup: 'exit'},
        output_actions=[(Bpod.OutputChannels.PWM1, 255)])

    my_bpod.send_state_machine(sma)

    my_bpod.run_state_machine(sma)

    print("Current trial info: {0}".format(my_bpod.session.current_trial))

    my_bpod.close()

As it can be seen from this example, the protocol written can be used either with the plugin or directly, with no
changes necessary to test the input and output ports and if the events are being triggered as expected.

The available input and output channel names, as well as the event names, for both the Bpod v0.7 and Bpod v2 are
presented in the next sections.

.. note::
    For either case of the Bpod's hardware version, it is assumed that firmware version **22** is installed.


..    include:: <isopub.txt>
Input channel names
===================
.. list-table::
    :widths: 15 11 11
    :header-rows: 1
    :align: center

    * - Input channel
      - Bpod v0.7
      - Bpod v2
    * - Serial1
      - |check|
      - |check|
    * - Serial2
      - |check|
      - |check|
    * - Serial3
      - |check|
      - |check|
    * - Serial4
      - |cross|
      - |check|
    * - Serial5
      - |cross|
      - |check|
    * - USB1
      - |check|
      - |check|
    * - BNC1
      - |check|
      - |check|
    * - BNC2
      - |check|
      - |check|
    * - Wire1
      - |check|
      - |cross|
    * - Wire2
      - |check|
      - |cross|
    * - Port1
      - |check|
      - |check|
    * - Port2
      - |check|
      - |check|
    * - Port3
      - |check|
      - |check|
    * - Port4
      - |check|
      - |check|
    * - Port5
      - |check|
      - |cross|
    * - Port6
      - |check|
      - |cross|
    * - Port7
      - |check|
      - |cross|
    * - Port8
      - |check|
      - |cross|
    * - GlobalTimer1
      - |check|
      - |check|
    * - GlobalTimer2
      - |check|
      - |check|
    * - GlobalTimer3
      - |check|
      - |check|
    * - GlobalTimer4
      - |check|
      - |check|
    * - GlobalTimer5
      - |check|
      - |check|
    * - GlobalTimer6
      - |cross|
      - |check|
    * - GlobalTimer7
      - |cross|
      - |check|
    * - GlobalTimer8
      - |cross|
      - |check|
    * - GlobalTimer9
      - |cross|
      - |check|
    * - GlobalTimer10
      - |cross|
      - |check|
    * - GlobalTimer11
      - |cross|
      - |check|
    * - GlobalTimer12
      - |cross|
      - |check|
    * - GlobalTimer13
      - |cross|
      - |check|
    * - GlobalTimer14
      - |cross|
      - |check|
    * - GlobalTimer15
      - |cross|
      - |check|
    * - GlobalTimer16
      - |cross|
      - |check|

Output channel names
====================

.. list-table::
    :widths: 15 11 11
    :header-rows: 1
    :align: center

    * - Output channel
      - Bpod v0.7
      - Bpod v2
    * - Serial1
      - |check|
      - |check|
    * - Serial2
      - |check|
      - |check|
    * - Serial3
      - |check|
      - |check|
    * - Serial4
      - |cross|
      - |check|
    * - Serial5
      - |cross|
      - |check|
    * - SoftCode
      - |check|
      - |check|
    * - BNC1
      - |check|
      - |check|
    * - BNC2
      - |check|
      - |check|
    * - Wire1
      - |check|
      - |cross|
    * - Wire2
      - |check|
      - |cross|
    * - Wire3
      - |check|
      - |cross|
    * - PWM1
      - |check|
      - |check|
    * - PWM2
      - |check|
      - |check|
    * - PWM3
      - |check|
      - |check|
    * - PWM4
      - |check|
      - |check|
    * - PWM5
      - |check|
      - |cross|
    * - PWM6
      - |check|
      - |cross|
    * - PWM7
      - |check|
      - |cross|
    * - PWM8
      - |check|
      - |cross|
    * - Valve1
      - |check|
      - |check|
    * - Valve2
      - |check|
      - |check|
    * - Valve3
      - |check|
      - |check|
    * - Valve4
      - |check|
      - |check|
    * - Valve5
      - |check|
      - |cross|
    * - Valve6
      - |check|
      - |cross|
    * - Valve7
      - |check|
      - |cross|
    * - Valve8
      - |check|
      - |cross|
    * - GlobalTimerTrig
      - |check|
      - |check|
    * - GlobalTimerCancel
      - |check|
      - |check|
    * - GlobalCounterReset
      - |check|
      - |check|

Event names
===========

.. note::
    In the following table, to reduce the size of the table, a convention was defined to aggregate several names of the
    events. For example, where it can be read Serial1_[1-15], it means that we can have Serial1_1, Serial1_2, until
    Serial1_15.

.. list-table::
    :widths: 15 11 11
    :header-rows: 1
    :align: center

    * - Event names
      - Bpod v0.7
      - Bpod v2
    * - Serial1_[1-15]
      - |check|
      - |check|
    * - Serial2_[1-15]
      - |check|
      - |check|
    * - Serial3_[1-15]
      - |check|
      - |check|
    * - Serial4_[1-15]
      - |cross|
      - |check|
    * - Serial5_[1-15]
      - |cross|
      - |check|
    * - SoftCode[1-15]
      - |check|
      - |check|
    * - BNC1High
      - |check|
      - |check|
    * - BNC1Low
      - |check|
      - |check|
    * - BNC2High
      - |check|
      - |check|
    * - BNC2Low
      - |check|
      - |check|
    * - Port1In
      - |check|
      - |check|
    * - Port1Out
      - |check|
      - |check|
    * - Port2In
      - |check|
      - |check|
    * - Port2Out
      - |check|
      - |check|
    * - Port3In
      - |check|
      - |check|
    * - Port3Out
      - |check|
      - |check|
    * - Port4In
      - |check|
      - |check|
    * - Port4Out
      - |check|
      - |check|
    * - Port5In
      - |check|
      - |cross|
    * - Port5Out
      - |check|
      - |cross|
    * - Port6In
      - |check|
      - |cross|
    * - Port6Out
      - |check|
      - |cross|
    * - Port7In
      - |check|
      - |cross|
    * - Port7Out
      - |check|
      - |cross|
    * - Port8In
      - |check|
      - |cross|
    * - Port8Out
      - |check|
      - |cross|
    * - GlobalTimer1_Start
      - |check|
      - |check|
    * - GlobalTimer2_Start
      - |check|
      - |check|
    * - GlobalTimer3_Start
      - |check|
      - |check|
    * - GlobalTimer4_Start
      - |check|
      - |check|
    * - GlobalTimer5_Start
      - |check|
      - |check|
    * - GlobalTimer6_Start
      - |cross|
      - |check|
    * - GlobalTimer7_Start
      - |cross|
      - |check|
    * - GlobalTimer8_Start
      - |cross|
      - |check|
    * - GlobalTimer9_Start
      - |cross|
      - |check|
    * - GlobalTimer10_Start
      - |cross|
      - |check|
    * - GlobalTimer11_Start
      - |cross|
      - |check|
    * - GlobalTimer12_Start
      - |cross|
      - |check|
    * - GlobalTimer13_Start
      - |cross|
      - |check|
    * - GlobalTimer14_Start
      - |cross|
      - |check|
    * - GlobalTimer15_Start
      - |cross|
      - |check|
    * - GlobalTimer16_Start
      - |cross|
      - |check|
    * - GlobalTimer1_End
      - |check|
      - |check|
    * - GlobalTimer2_End
      - |check|
      - |check|
    * - GlobalTimer3_End
      - |check|
      - |check|
    * - GlobalTimer4_End
      - |check|
      - |check|
    * - GlobalTimer5_End
      - |check|
      - |check|
    * - GlobalTimer6_End
      - |cross|
      - |check|
    * - GlobalTimer7_End
      - |cross|
      - |check|
    * - GlobalTimer8_End
      - |cross|
      - |check|
    * - GlobalTimer9_End
      - |cross|
      - |check|
    * - GlobalTimer10_End
      - |cross|
      - |check|
    * - GlobalTimer11_End
      - |cross|
      - |check|
    * - GlobalTimer12_End
      - |cross|
      - |check|
    * - GlobalTimer13_End
      - |cross|
      - |check|
    * - GlobalTimer14_End
      - |cross|
      - |check|
    * - GlobalTimer15_End
      - |cross|
      - |check|
    * - GlobalTimer16_End
      - |cross|
      - |check|
    * - GlobalCounter1_End
      - |check|
      - |check|
    * - GlobalCounter2_End
      - |check|
      - |check|
    * - GlobalCounter3_End
      - |check|
      - |check|
    * - GlobalCounter4_End
      - |check|
      - |check|
    * - GlobalCounter5_End
      - |check|
      - |check|
    * - GlobalCounter6_End
      - |cross|
      - |check|
    * - GlobalCounter7_End
      - |cross|
      - |check|
    * - GlobalCounter8_End
      - |cross|
      - |check|
    * - Condition1
      - |check|
      - |check|
    * - Condition2
      - |check|
      - |check|
    * - Condition3
      - |check|
      - |check|
    * - Condition4
      - |check|
      - |check|
    * - Condition5
      - |check|
      - |check|
    * - Condition6
      - |cross|
      - |check|
    * - Condition7
      - |cross|
      - |check|
    * - Condition8
      - |cross|
      - |check|
    * - Condition9
      - |cross|
      - |check|
    * - Condition10
      - |cross|
      - |check|
    * - Condition11
      - |cross|
      - |check|
    * - Condition12
      - |cross|
      - |check|
    * - Condition13
      - |cross|
      - |check|
    * - Condition14
      - |cross|
      - |check|
    * - Condition15
      - |cross|
      - |check|
    * - Condition16
      - |cross|
      - |check|
    * - Tup
      - |check|
      - |check|
