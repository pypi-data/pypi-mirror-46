
============
Introduction
============

PieTunes is a Python library that creates an abstraction of
Apple's Scripting Bridge API for iTunes. This makes it much easier to
write Python scripts (or full python applications) that interact with
iTunes and the iTunes Store.

There are some caveats:
    * The only external dependency right now is
      `PyObjC <https://pythonhosted.org/pyobjc/index.html>`_
    * Due to this dependency, this pietunes Python library is only available
      for MacOS [#f1]_
    * This is a modern Python library that requires ``Python>=3.6``


Objectives
----------
#. Create a modern, stable Python library with a clearly-defined API  
#. Provide as close to 100% Test Coverage as possible [#f2]_
#. Provide clear documentation with full coverage of the API and example code.



Installing
----------

Install and update using `pip`:

.. code-block:: bash

   pip install -U pietunes


A Simple Example
----------------

.. code-block:: python

   from pietunes import App

   app = App()

   def _get_all_playlists():
       return app.playlists


Links
-----

* Website: https://pypi.org/project/pietunes/
* Documentation: https://brianfarrell.gitlab.io/pietunes/
* License: https://www.gnu.org/licenses/agpl.html
* Releases: https://pypi.org/project/pietunes/
* Code: https://gitlab.com/brianfarrell/pietunes/
* Issue tracker:
* Test status:
* Test coverage:

.. rubric:: Footnotes

.. [#f1] Once this is working correctly on MacOS, I will look into how
        I might possibly get it working for iTunes on Windows.

.. [#f2] | This project started-out as a Proof of Concept (POC).
       | At that point, no automated testing was involved.
       | Going forward, all new development and bug fixes will be test-driven.
