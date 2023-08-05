==================
Setting up a trial
==================

Setting up a trial to use the minimization method requires
you to choose a few settings, based on the design of the
trial and what you think will be most important
to balance. These are:

* The :ref:`arms <arms>` that participants will be assigned to.
* The prognostic :ref:`factors <factors>` that need to be balanced.
* The function that calculates the amount of imbalance
  :ref:`within each factor <d_function>`
* The function that combines the factor imbalance scores to
  find the :ref:`total imbalance <total_function>`
* How :ref:`probabilities <probs>` will be assigned to
  each arm, based on the imbalance scores.

Some of those pieces might require additional settings, e.g.
providing the probability that the most favoured arm
will be assigned.

Putting these all together, a full specification for
a trial might look like:

.. testcode::

    from smallerize import Arm, Factor, Minimizer

    arms = [Arm('Control', allocation_ratio=1),
            Arm('Active', allocation_ratio=2)]
    factors = [Factor('Sex', levels=['Female', 'Male']),
               Factor('Site', levels=['Site A', 'Site B', 'Site C'])]

    minimizer = Minimizer(
        factors=factors,
        arms=arms,
        d_imbalance_method='marginal_balance',
        total_imbalance_method='sum',
        probability_method='biased_coin',
        preferred_p=0.8
    )

.. _arms:

Trial arms
----------

First we outline all the arms that participants
will be assigned to.

* Each arm requires a unique name
* Each arm might have a different allocation
  ratio, if the trial design requires different
  proportions in each group. This is optional,
  if you don't provide them all arms will be assigned
  in equal proportions.

Example:

.. testcode::

    # Equal allocation ratios
    equal_arms = [Arm('Placebo'), Arm('Surgery')]
    # Different allocation ratios
    unbalanced_arms = [
        Arm('Control', allocation_ratio=1),
        Arm('Active', allocation_ratio=2),
        Arm('Waitlist', allocation_ratio=1)
    ]

.. note::

    When using unequal allocation ratios, you might want
    to use the 'biased coin' method to assign probabilities

.. _factors:

Factors
-------

Factors are participant characteristics that we want
to balance because they might affect the trial
outcomes. The minimization method allows you to
balance participants across multiple factors
simultaneously - unlike in stratification methods,
this doesn't split participants up into increasingly
small strata.

Factors must be categorical - they must have a finite
set of levels that each participant will match up
to.

* Each factor requires a unique name.
* Each factor will have its own factor levels.
* *(Optional):* factors can be given different weights, so
  that they contribute different amounts to the total imbalance
  score. When using different weights, you must use the
  "weighted sum" method to calculate the total imbalance
  score.

Examples:

.. testcode::

    sex = Factor('Sex', levels=['Female', 'Male'])
    # Factors must be categorical - bin numeric variables
    age = Factor('Age', levels=['20-29', '30-39', '40+'])
    # Optional weights
    weighted = [
        Factor('Severity', levels=['Low', 'High'], weight=2.0),
        Factor('Sex', levels=['Female', 'Male'], weight=1.0)
    ]

.. _d_function:

Imbalance within each factor
----------------------------

When assigning a new participant, we could consider
what would happen if the new participant was assigned
to each arm.

Within each factor, we look at the current participants
who match the new participant's factor level, e.g.
if for sex we currently have

========  ==========  ============
Arm        Male         Female
========  ==========  ============
Placebo      9            11
Active      12             8
========  ==========  ============

and we are assigning a female participant, then
assigning the participant to Placebo would result
in ``Placebo: 12, Active: 8`` and assigning them
to Active would result in ``Placebo: 11, Active: 9``.
While assigning a female participant, the number of male
participants assigned to each arm doesn't contribute
to any imbalance calculations.

We take these potential counts, and use a function
that scores the amount of imbalance between arms. E.g.
if we use the range, then assigning to Placebo would
give :math:`\text{range}(12, 8) = 4` and assigning
to Active would give :math:`\text{range}(11, 9) = 2`.

From Pocock + Simon (1975) and Han (2009), the different
functions we can use for ``d_imbalance_method`` are:

* ``'range'``: The highest count in an arm minus the smallest.
* ``'standard_deviation'``: The standard deviation of counts.
* ``'variance'``: Variance. Assigns an increasingly high
  score to large amounts of imbalance, so may be better at preventing
  extreme imbalance than the range or standard deviation.
* ``'over_max_range'``: A binary indicator that is 1 if the
  range exceeds a specified threshold, and 0 otherwise.

    - If using this function, you must also supply the threshold as
      an additional argument ``d_max_range``, e.g. ``d_max_range=2``
* ``'is_largest'``: A binary indicator that is 1 if the
  potential arm will have the highest count, and 0 otherwise (only
  works when the trial has exactly 2 arms).
* ``'marginal_balance'``: A relative measure between 0.0 (all
  treatments equal) and 1.0 (all participants in 1 treatment),
  as outlined in Han (2009). Weights factor levels with many
  participants lower, so that rare factor levels also contribute
  to the total imbalance.

We carry out this calculation for each factor, generating
a set of scores like:

+---------------+---------------------+----------------------+
| Potential arm | Resulting imbalance | Resulting imbalance  |
|               | within Sex          | within Severity      |
+===============+=====================+======================+
| Placebo       | 2                   | 1                    |
+---------------+---------------------+----------------------+
| Active        | 1                   | 3                    |
+---------------+---------------------+----------------------+

.. note::

   When arms have different allocation ratios, we divide the
   count in each arm by its allocation ratio first, meaning
   the degree of imbalance is calculated relative to
   the desired counts. This doesn't entirely account for
   the different allocation ratios though, so using
   the ``'biased_coin'`` method to assign probabilities
   is still recommended.

Examples:

.. testcode::

    minimizer = Minimizer(
        factors=[sex, age],
        arms=[Arm('Placebo'), Arm('Active')],
        d_imbalance_method='over_max_range',
        # over_max_range requires an additional argument
        d_max_range=3
    )

.. testoutput::

    preferred_p argument was not provided. Using default value of 0.75

.. _total_function:

Total imbalance
---------------

Once we have the degree of imbalance within each factor,
we combine them into a total score, the overall imbalance
that would result from assigning each potential arm.
We can just use the sum here, although we can also apply
different weights to each factor and use a weighted sum. Valid
values for ``total_imbalance_method`` are:

* ``'sum'``
* ``'weighted_sum'``: Weight the sum by the ``weight`` attribute
  of each factor.

E.g. using the table above with Sex and Severity, and
using the sum to combine scores, assigning to Placebo
would result in a score of 3, and assigning to
Active would result in a score of 4.

.. _probs:

Assigning probabilities
-----------------------

After we have the total imbalance that would result from
assigning the new participant to each arm, we rank
the arms in increasing order of imbalance, and
apply different probabilities. The different options
for ``probability_method`` are:

* ``'best_only'``: The arm that would result in the
  least imbalance is assigned with a high probability, and
  the remaining probability is divided among the remaining
  arms.

    - An additional argument ``preferred_p`` sets the probability
      for the arm with lowest imbalance, e.g. ``preferred_p=0.7``.
      Setting this to 1.0 means the arm that produces the lowest
      imbalance is always assigned, but may make the allocation
      sequence too predictable.

* ``'rank_all'``: The full ranking of arms is taken into account,
  with each successive arm being assigned a lower probability
  than the last.

    - An additional argument ``q`` sets the degree to which
      the arm with lowest imbalance is favoured. ``q`` must
      be between :math:`1 / N` and :math:`2 / (N - 1)`, where
      :math:`N` is the number of arms in the trial, and
      higher values mean the arm with lower imbalance is
      favoured more. E.g. with :math:`N = 4, q = 1 / 2`,
      the probabilities assigned are 0.4, 0.3, 0.2, 0.1.

* ``'biased_coin'``: The biased-coin minimization method
  outlined in Han (2009), which correctly accounts for
  trials where arms have different allocation ratios.

    - An additional argument ``preferred_p`` sets the probability
      that the arm with the lowest allocation ratio
      will be assigned, when it produces the lowest imbalance.
      Arms with other allocation ratios have their
      probabilities adjusted accordingly.
