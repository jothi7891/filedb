# weta
Here is a file like database with very minimalistic functions as exepcted.

### Notes:

* There is only change in the way the arguments are give just because `argparse` does not parse quotes strings well.

While giving the `filter` arguments, it should be enclosed in double quotes and the arguments for individual filter fields should be
given in single quotes and not the other way around.
```shell

"PROJECT='the hobbit' OR PROJECT='king kong'"
```



* This is more a prototype and not necessarily a very high performing one as I am using
json as the backend and many places where performance was traded for 
readability and ease.

* Implemented all the four tasks and done a few basic tests and hooked up to 
circle CI to run the tests

* There are definitely few places where I hacked a bit like implementing the database layer 
without the tables or collection layer , just was not able to get time to put it through

* Also , few try and except are missing in some places which should have been done and again if tim permitted would have done




