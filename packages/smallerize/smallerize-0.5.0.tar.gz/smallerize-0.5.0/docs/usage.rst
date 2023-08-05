=====
Usage
=====

To use smallerize in a project:

.. testcode::

    import smallerize

Or:

.. testcode::

    from smallerize import Arm, Factor, Minimizer

A simple example of setting up a trial and assigning a participant
is:

.. testcode::

    from smallerize import Arm, Factor, Minimizer

    sex = Factor('Sex', levels=['Male', 'Female'])
    site = Factor('Site', levels=['A', 'B', 'C'])

    minimizer = Minimizer(
        factors=[sex, site],
        arms=[Arm('Treat'), Arm('Control')],
        d_imbalance_method='standard_deviation',
        probability_method='best_only',
        preferred_p=0.75
    )

    new_participant = {'Sex': 'Female', 'Site': 'B'}
    assigned_arm = minimizer.assign_participant(new_participant)

Simulation
----------

You can also use the ``simulate`` module to compare the performance
of different allocation methods and settings:

.. testcode::

    from smallerize import simulate

See :doc:`the API docs </api>` for further details..