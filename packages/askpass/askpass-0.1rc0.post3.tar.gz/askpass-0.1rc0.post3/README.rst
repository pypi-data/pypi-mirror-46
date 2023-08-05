|pipeline| |coverage| |rtd|

.. |pipeline| image:: https://framagit.org/1ohmatr/sw/py/askpass.git/badges/master/pipeline.svg

.. |coverage| image:: https://framagit.org/1ohmatr/sw/py/askpass.git/badges/master/coverage.svg

.. |rtd| image:: https://readthedocs.org/projects/askpass/badge/?version=latest

Wrapper for the pinentry program. Easy workflow in python:

.. code:: python

  from askpass import AskPass

  with AskPass() as ask:
    for x in ask:
      if x == 'password': break
    else:
      raise ValueError()
