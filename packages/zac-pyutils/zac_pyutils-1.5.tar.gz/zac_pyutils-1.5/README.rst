PyTree
======
.. image:: https://img.shields.io/pypi/v/tree.svg?style=flat-square
        :target: https://pypi.python.org/pypi/Tree

.. image:: https://img.shields.io/pypi/l/Tree.svg?style=flat-square
        :target: https://github.com/PixelwarStudio/PyTree/blob/master/LICENSE

Python package, which you can use to generate and drawing trees, realistic or fractal ones.

Usage
-----
.. code-block:: bash

    $ pip install zac-pyutils  --upgrade -i https://pypi.python.org/pypi

.. code-block:: python

    from zac_pyutils import ExqUtils
    # log to file
    logger = ExqUtils.get_logger("tmp.log")
    ExqUtils.log2file(message="new message",logger=logger)
    # load file as iter
    fileIter = ExqUtils.load_file_as_iter("./data/nlp/sample_data.txt")
