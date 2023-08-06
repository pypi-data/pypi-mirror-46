=======
History
=======

0.1.0 (2019-03-13)
------------------

* First release on PyPI.


0.2.0 (2019-03-20)
------------------
* Completed the Tweet class that allows the user to make usable instances of a
  tweet model. Includes initialization of all the Tweet attributes indicated in
  the Twitter documentation (default to None, unless the user provides a value)
  and overriding of __getitem__ to provide a dictionary-like access to the
  information.


0.3.0 (2019-03-20)
------------------
* Added method "get_tweets_from_csv()", which gets a CSV file as an argument
  and returns a list containing as many Tweet objects as lines (minus the
  header) in the CSV file. The header of the CSV is used to know which 
  attributes should be set.
* The method will raise an error and exit if any item in the header does not
  match with the specification of the Tweet object (for example, the header
  word "media.sizes.thumb.h" would be valid, but "user.lightsaber.color" would
  not.
* At this point, the method took 1.75s aprox to read and return the contents of
  a 5.7 MB as a list of 'Tweet's. This could be troublesome with very large
  collections in a future if the progression of time was proportional with the 
  file size (estimation would be 25 minutes for a 5 GB file)
  

0.4.0 (2019-03-26)
------------------
    
Since the last release the main improvements have been:

 * Raise a custom exception instead of sysexiting when confronted with a wrong 
   CSV file.
 * Change prints for logger messages.
 * Modularize the "get_tweets_from_csv" dividing it into 3 functions to provide
   more isolated functions. Now this function makes use of 
   "get_tweet_from_csv_line", which returns a single Tweet object when provided 
   with two lists representing the contents of a CSV header and one of its
   entries. There is also a "raw" alternative of that function, which works 
   with raw lines and converts them to lists to then call the "non-raw" version.

Version 0.4.1:
The tweet-manager dependency, necessary for the core functions, has been added 
into production (in setup.py).
Version 0.4.2:
Seems like that wasn't the right way to add a requirement. Tried now pip
freezing to requirements.txt.
Version 0.4.3:
Updated tweetmanager dependency to current version (1.1.5)
Version 0.4.4:
Fixed another requirement error
Version 0.4.5:
Changed f-strings to traditional strings for reasons of compatibility
Version 0.4.6:
Trying to track an error were Tweets are not instantiated if the CSV registry
contains certain symbols
Version 0.4.7:
Added function to generate dicts representing subsets of Tweet content (return
just the fields indicated by the user and not the full Tweet object)


0.5.0 (2019-05-03)
------------------
* Code from tweet_model.py now divided in two source files: tweet.py
  (containing the Tweet class) and utils.py (which contains the rest of the
  utilities to instantiate Tweet objects from CSVs, return a mini-dict with
  partial information of a Tweet, etc.)
* Added two new fields to the Tweet class: "polarity" and "trtext", which are
  not part of the original Tweeter tweets, but needed in other project.
* Added setter methods for "polarity" and "trtext", which will be probably now
  set at instantiation time but afterwards

Version 0.5.1:
Tiny fix in the imports
Version 0.5.2:
Added method to get Tweet in JSON form
