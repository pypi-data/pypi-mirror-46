``fix_yahoo_finance`` was renamed to ``yfinance``
=================================================

This library was renamed to ``yfinance``.
For reasons of backward-competability, this library is importing
and using ``yfinance`` - but you should install and use
``yfinance`` directly.

### 1. Install using ``pip``:

.. code:: bash

    $ pip install yfinance --upgrade --no-cache-dir


### 2. Change your code to import ``yfinance`` instead of ``fix_yahoo_finance``:

.. code:: python

    import yfinance as yf


