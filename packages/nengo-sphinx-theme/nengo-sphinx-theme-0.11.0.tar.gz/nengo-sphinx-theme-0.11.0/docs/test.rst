************
Feature test
************

This page contains examples of various features of the Nengo theme.
It is mainly useful for internal testing
to make sure everything is displaying correctly.
This page is based on the `Cloud Sphinx theme's feature test
<https://cloud-sptheme.readthedocs.io/en/latest/cloud_theme_test.html>`_.

Styling
=======

Sub-headings
------------

Sub-sub-headings
^^^^^^^^^^^^^^^^

Sub-sub-sub-headings
####################

Text
----

Inline literal: ``literal text``

External link: `<http://www.google.com>`_

Email link: bob@example.com

**Bold text**

*Italic text*

Math
----

Inline math: :math:`a^2 + b^2 = c^2`

Displayed math, with a label:

.. math:: e^{i\pi} + 1 = 0
   :label: euler

Equation reference: :eq:`euler`

Admonitions
-----------

.. note:: This is a note.

.. caution:: This is slightly dangerous.

.. warning:: This is a warning.

.. danger:: This is dangerous.

.. seealso:: This is a "see also" message.

.. todo:: This is a todo message.

   With some additional next on another line.

.. deprecated:: 0.1

   This is a deprecation warning.

.. versionadded:: 0.1

   This was added.

.. versionchanged:: 0.1

   This was changed.

Code
----

Python code block with line numbers:

.. code-block:: python
   :linenos:

   >>> import os

   >>> os.listdir("/home")
   ['bread', 'pudding']

   >>> os.listdir("/root")
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   OSError: [Errno 13] Permission denied: '/root'

INI code block:

.. code-block:: ini

   [rueben]
   bread = rye
   meat = corned beef
   veg = sauerkraut

Documentation
-------------

Function:

.. function:: frobfunc(foo=1, *, bar=False)

    :param foo: foobinate strength
    :type foo: int

    :param bar: enabled barring.
    :type bar: bool

    :returns: frobbed return
    :rtype: str

    :raises TypeError: if *foo* is out of range

Class:

.. class:: FrobClass(foo=1, *, bar=False)

    Class docstring. Saying things.

    .. attribute:: foo

        foobinate strength

    .. attribute:: bar

        barring enabled

    .. method:: run()

        execute action, return result.

Tables
------

.. table:: Normal Table

    =========== =========== ===========
    Header1     Header2     Header3
    =========== =========== ===========
    Row 1       Row 1       Row 1
    Row 2       Row 2       Row 2
    Row 3       Row 3       Row 3
    =========== =========== ===========

.. rst-class:: fullwidth

.. table:: Full Width Table

    =========== =========== ===========
    Header1     Header2     Header3
    =========== =========== ===========
    Row 1       Row 1       Row 1
    Row 2       Row 2       Row 2
    Row 3       Row 3       Row 3
    =========== =========== ===========

Extensions
==========

Versioning
----------

:doc:`deeply/nested/testing/page`
versioned links work properly.
