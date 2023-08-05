============
Minimization
============

.. note::

    This page tries to summarize the details of how minimization
    works as a method of treatment allocation. It mostly
    just summarises the original Pocock and Simon article
    `found here <https://doi.org/10.2307/2529712>`_

Minimization balances treatment assignments across multiple
prognostic factors simultaneously. Let's start with some notation - we're
running a trial and we have:

* :math:`N` different treatments to assign participants to.
* :math:`M` prognostic factors that we want to balance
  (all categorical [#cont_factors]_).

  * Each factor has :math:`n_i` levels.

At any point during the trial, :math:`x_{ijk}` is the number of participants
assigned to treatment :math:`k`, who have level :math:`j` of factor :math:`i`.

A new patient coming into the trial has a factor level for each of the
:math:`M` factors :math:`r_1, \dots, r_M`. If that patient is assigned to
treatment :math:`k`, there will be new values :math:`x_{ijl}^k`:

.. math::

   x_{i r_i k}^k = x_{ijk} + 1

.. math::

   x_{ijl}^k = x_{ijl} \text{ for } l \neq k, j \neq r_i


i.e. we add 1 to all the counts :math:`x_{ijk}` that match the treatment
:math:`k` and the factor levels the participant has, and all the other
counts are unchanged.

Calculating imbalance
---------------------

Imbalance within each factor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We start by calculating the imbalance within each factor.
We choose a function :math:`D(\{ z \})` that measures the variation in
the participant counts :math:`\{ z \}` (you can choose different functions
like :math:`D = \text{range}`). For each treatment :math:`k` that a new
participant could be assigned to, we can get the resulting
counts that would be produced by assigning to :math:`k`, and calculate:

.. math::

    d_{ik} = D( \{ x_{i r_i l}^k \}_{l = 1}^N)

i.e. the imbalance in treatment numbers across all treatments,
for all participants with level :math:`r_i` on factor :math:`i`.

.. note::

    Only participants who match the new participant's
    factor level :math:`r_i` matter for the calculation of
    imbalance for factor :math:`i`,
    participants with other factor levels don't affect the
    imbalance calculation

Total imbalance
^^^^^^^^^^^^^^^

Once we have the imbalance within each factor, we combine
them to produce a total imbalance score. We choose
a function :math:`G` and calculate

.. math::

    G_k = G(d_{1k}, \cdots, d_{Mk})

that combines the :math:`d_{ik}` for all the :math:`M` factors
(an obvious choice for :math:`G` is just the sum). Then :math:`G_k` is the total
imbalance you would have, if the new patient is assigned to treatment :math:`k`.
We calculate :math:`G_k` for all the :math:`N` treatments.

Assigning probabilities
^^^^^^^^^^^^^^^^^^^^^^^

You can then rank the treatments in order of increasing
:math:`G_k` values (increasing = larger amount of imbalance),
assigning ascending ranks :math:`(1), (2), \dots, (N)`.

Then pick some way of assigning decreasing probabilities
of treatment assignment :math:`p_k` to these, i.e.

.. math::

    p_1 \geq p_2 \geq \cdots \geq p_N

(:math:`p_k` could be a function of :math:`G_k`, the amount of imbalance,
but this may be unnecessarily complex, and in practice just
using the ranks should produce good balance).

Additional details
------------------

Unequal treatment allocation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Han et al. (2009) <https://doi.org/10.1002/sim.3710>`_ discussed
how minimization could be adapted to trials with unequal
treatment allocation ratios.

The original minimization method can be adapted by simply
dividing the count of participants in each arm (within each factor)
by that arm's allocation ratio - e.g. if the allocation ratio
is 1:2 and the current counts for female participants are 11 and 20,
then we would divide and get 11 and 10 - and then calculate
the factor imbalance score from these values.

However this method is not perfect, as it results in a bias:
slightly more participants are allocated to arms with low
allocation ratios than desired, and slightly less to arms
with high allocation ratios. Han et al. (2009) also propose
a "biased coin minimization" method that solves this issue.

Biased coin minimization
""""""""""""""""""""""""

In the biased coin minimization method, the treatment
that would produce least imbalance is assigned with
a probability given by:

.. math::

    p^H_{(i)} = 1 - \frac{
            \sum_{k \neq i}^N r_{(k)}
        }{
            \sum_{k \neq 1}^N r_{(k)}
        } \left( 1 - p^H_{(1)} \right)

where :math:`p^H_{(1)}` is the probability that the treatment
with the lowest allocation ratio will be assigned, when
it produces the lowest imbalance.

The remaining probability is divided between treatments according
to the formula:

.. math::

    p^L_{(i), H = (j)} =
        \frac{
            r_{(i)}
        }{
            \sum_{k \neq j}^N r_{(k)}
        } \left( 1 - p^H_{(j)} \right)



.. rubric:: Footnotes

.. [#cont_factors] Continuous factors can be accounted for in some extensions
   of the minimization method, but they are not implemented in ``smallerize``
