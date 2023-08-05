===========
tweetmagick
===========
Generate images with tweet-like appearance

Installation
------------
::

    pip3 install tweetmagick

Examples
--------


.. code-block:: python

    from tweetmagick import TweetGenerator

    name = "harold"
    longname = "stockmaster"
    avatar = "harold.jpg"
    text = "feeling pompous today, might delete later"
    with TweetGenerator(name, longname, avatar, text) as tg:
        tg.tweetgen(debug=True)

Code above will display the image and exit without saving it.

``tweetgen`` method returns BytesIO object with png binary blob.
Below is the code that will save your image to a file:

.. code-block:: python

    from shutil import copyfileobj

    with TweetGenerator(name, longname, avatar, text, theme="light") as tg:
        with open("haroldtweets.png", "wb") as tweet:
            copyfileobj(tg.tweetgen(), tweet)

Results in :

.. image:: haroldtweets.png
    :align: left

With ``dark`` theme option:

.. image:: haroldtweetsduringnight.png
    :align: left



TODO
~~~~
Implement some streamlined method for embedding images in tweets.

Also some method for reply/quote images
