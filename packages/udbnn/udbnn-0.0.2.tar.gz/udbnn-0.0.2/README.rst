Umbalanced dataset-aware batch-size neural networks
================================================================================================
|travis| |sonar_quality| |sonar_maintainability| |sonar_coverage| |code_climate_maintainability|

Experiment to determine whetever a large batch-size can be helpful with extremely umbalanced datasets.

How do I get this?
------------------------------
Just run:

.. code:: shell

   pip install tensorflow # or tensorflow-gpu, whetever you have a gpu or not
   git clone https://github.com/LucaCappelletti94/udbnn.git
   cd udbnn
   pip install .

How do I run the experiments?
--------------------------------
Since the experiments take quite a bit to run, I suggest you to run them while in a TMUX-like environment. If available, you should consider using a computer with a tensorflow-compatible GPU.

Then just run with a python shell:

.. code:: python

   from udbnn import run
   run("dataset")


.. |travis| image:: https://travis-ci.org/LucaCappelletti94/udbnn.png
   :target: https://travis-ci.org/LucaCappelletti94/udbnn

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_udbnn&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_udbnn

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_udbnn&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_udbnn

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_udbnn&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_udbnn

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/25fb7c6119e188dbd12c/maintainability
   :target: https://codeclimate.com/github/LucaCappelletti94/udbnn/maintainability
   :alt: Maintainability
