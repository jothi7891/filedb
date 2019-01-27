# weta
Here is a file like database with very minimalistic functions as exepcted.

### Notes:

* There is only change in the way the arguments are give just because `argparse` does not parse quotes strings well.

While giving the `filter` arguments, it should be enclosed in double quotes and the arguments for individual filter fields should be
given in single quotes and not the other way around.
```shell

"PROJECT='the hobbit' OR PROJECT='king kong'"

instead of

'PROJECT="the hobbit" OR PROJECT="lotr"'
```

* This is more a prototype and not necessarily a very high performing one as I am using
json as the backend and many places where performance was traded for 
readability and ease.

* Implemented all the four tasks and done a few basic tests and hooked up to 
circle CI to run the tests

* There are definitely few places where I hacked a bit like implementing the database layer 
without the tables or collection layer , just was not able to get time to put it through

* Also , few try and except are missing in some places which should have been done and again if time permitted would have done.

* The `order_by` does not support ordering by aggregates yet.

* The only external library used is `pytest` for conducting tests.


### Command Usages and Examples
There is an -i, -r and - f option to provide the input file, remove database and start from scratch and also provide the 
location of the db file..
```shell
python3 -m load

python3 -m load -f "filedb/db.json" -r -i "data/input.txt"

(weta) bash-3.2$ python3 -m load -f "filedb/db.json" -r True -i "data/input.txt"
INFO:__main__: Inside the load
INFO:filedb.datastore:Db file already exists
INFO:filedb.loader:validating the header info
INFO:filedb.loader:validating the header line
INFO:filedb.loader:validated and transform the fields line
INFO:filedb.loader:validating field the hobbit against its defined properties
INFO:filedb.loader:The field the hobbit validity against its property is True
INFO:filedb.loader:validating field 45 against its defined properties
INFO:filedb.loader:The field 45 validity against its property is True
INFO:filedb.loader:validating field 64 against its defined properties
INFO:filedb.loader:The field 64 validity against its property is True
INFO:filedb.loader:validating field scheduled against its defined properties
INFO:filedb.loader:The field scheduled validity against its property is True
INFO:filedb.loader:validating field 2010-05-20 against its defined properties
INFO:filedb.loader:The field 2010-05-20 validity against its property is True
INFO:filedb.loader:validating field 45.00 against its defined properties
INFO:filedb.loader:The field 45.00 validity against its property is True
INFO:filedb.loader:validating field 2010-04-01 13:35 against its defined properties
INFO:filedb.loader:The field 2010-04-01 13:35 validity against its property is True
INFO:filedb.loader:The line the hobbit|45|64|scheduled|2010-05-20|45.00|2010-04-01 13:35 is validated successfully against the property
INFO:filedb.loader:validated and transform the fields line
INFO:filedb.loader:validating field lotr against its defined properties
INFO:filedb.loader:The field lotr validity against its property is True
INFO:filedb.loader:validating field 03 against its defined properties
INFO:filedb.loader:The field 03 validity against its property is True
INFO:filedb.loader:validating field 16 against its defined properties
INFO:filedb.loader:The field 16 validity against its property is True
INFO:filedb.loader:validating field finished against its defined properties
INFO:filedb.loader:The field finished validity against its property is True
INFO:filedb.loader:validating field 2001-10-15 against its defined properties
INFO:filedb.loader:The field 2001-10-15 validity against its property is True
INFO:filedb.loader:validating field 45.00 against its defined properties
INFO:filedb.loader:The field 45.00 validity against its property is True
INFO:filedb.loader:validating field 2001-04-01 06:47 against its defined properties
INFO:filedb.loader:The field 2001-04-01 06:47 validity against its property is True
INFO:filedb.loader:The line lotr|03|16|finished|2001-10-15|45.00|2001-04-01 06:47 is validated successfully against the property
INFO:filedb.loader:validated and transform the fields line
INFO:filedb.loader:validating field king kong against its defined properties
INFO:filedb.loader:The field king kong validity against its property is True
INFO:filedb.loader:validating field 42 against its defined properties
INFO:filedb.loader:The field 42 validity against its property is True
INFO:filedb.loader:validating field 128 against its defined properties
INFO:filedb.loader:The field 128 validity against its property is True
INFO:filedb.loader:validating field scheduled against its defined properties
INFO:filedb.loader:The field scheduled validity against its property is True
INFO:filedb.loader:validating field 2006-07-22 against its defined properties
INFO:filedb.loader:The field 2006-07-22 validity against its property is True
INFO:filedb.loader:validating field 25 against its defined properties
INFO:filedb.loader:The field 25 validity against its property is True
INFO:filedb.loader:validating field 2006-08-04 07:22 against its defined properties
INFO:filedb.loader:The field 2006-08-04 07:22 validity against its property is True
INFO:filedb.loader:The line king kong|42|128|scheduled|2006-07-22|25|2006-08-04 07:22 is validated successfully against the property
INFO:filedb.loader:validated and transform the fields line
INFO:filedb.loader:validating field the hobbit against its defined properties
INFO:filedb.loader:The field the hobbit validity against its property is True
INFO:filedb.loader:validating field null against its defined properties
INFO:filedb.loader:The field null validity against its property is True
INFO:filedb.loader:validating field 32 against its defined properties
INFO:filedb.loader:The field 32 validity against its property is True
INFO:filedb.loader:validating field finished against its defined properties
INFO:filedb.loader:The field finished validity against its property is True
INFO:filedb.loader:validating field 2010-05-15 against its defined properties
INFO:filedb.loader:The field 2010-05-15 validity against its property is True
INFO:filedb.loader:validating field 22.80 against its defined properties
INFO:filedb.loader:The field 22.80 validity against its property is True
INFO:filedb.loader:validating field 2010-03-22 01:10 against its defined properties
INFO:filedb.loader:The field 2010-03-22 01:10 validity against its property is True
INFO:filedb.loader:The line the hobbit|null|32|finished|2010-05-15|22.80|2010-03-22 01:10 is validated successfully against the property
INFO:filedb.loader:validated and transform the fields line
INFO:filedb.loader:validating field king kong against its defined properties
INFO:filedb.loader:The field king kong validity against its property is True
INFO:filedb.loader:validating field 42 against its defined properties
INFO:filedb.loader:The field 42 validity against its property is True
INFO:filedb.loader:validating field 128 against its defined properties
INFO:filedb.loader:The field 128 validity against its property is True
INFO:filedb.loader:validating field not required against its defined properties
INFO:filedb.loader:The field not required validity against its property is True
INFO:filedb.loader:validating field 2006-07-22 against its defined properties
INFO:filedb.loader:The field 2006-07-22 validity against its property is True
INFO:filedb.loader:validating field 35.00 against its defined properties
INFO:filedb.loader:The field 35.00 validity against its property is True
INFO:filedb.loader:validating field 2006-10-15 09:14 against its defined properties
INFO:filedb.loader:The field 2006-10-15 09:14 validity against its property is True
INFO:filedb.loader:The line king kong|42|128|not required|2006-07-22|35.00|2006-10-15 09:14 is validated successfully against the property
INFO:filedb.loader:validated and transform the fields line
INFO:filedb.loader:validating field king kong against its defined properties
INFO:filedb.loader:The field king kong validity against its property is True
INFO:filedb.loader:validating field 65 against its defined properties
INFO:filedb.loader:The field 65 validity against its property is True
INFO:filedb.loader:validating field 128 against its defined properties
INFO:filedb.loader:The field 128 validity against its property is True
INFO:filedb.loader:validating field not required against its defined properties
INFO:filedb.loader:The field not required validity against its property is True
INFO:filedb.loader:validating field 2006-07-22 against its defined properties
INFO:filedb.loader:The field 2006-07-22 validity against its property is True
INFO:filedb.loader:validating field 30.00 against its defined properties
INFO:filedb.loader:The field 30.00 validity against its property is True
INFO:filedb.loader:validating field 2006-10-15 09:14 against its defined properties
INFO:filedb.loader:The field 2006-10-15 09:14 validity against its property is True
INFO:filedb.loader:The line king kong|65|128|not required|2006-07-22|30.00|2006-10-15 09:14 is validated successfully against the property
INFO:filedb.loader:validated and transform the fields line
INFO:filedb.loader:validating field Avengers against its defined properties
INFO:filedb.loader:The field Avengers validity against its property is True
INFO:filedb.loader:validating field 45 against its defined properties
INFO:filedb.loader:The field 45 validity against its property is True
INFO:filedb.loader:validating field 64 against its defined properties
INFO:filedb.loader:The field 64 validity against its property is True
INFO:filedb.loader:validating field scheduled against its defined properties
INFO:filedb.loader:The field scheduled validity against its property is True
INFO:filedb.loader:validating field 2010-05-20 against its defined properties
INFO:filedb.loader:The field 2010-05-20 validity against its property is True
INFO:filedb.loader:validating field 45.00 against its defined properties
INFO:filedb.loader:The field 45.00 validity against its property is True
INFO:filedb.loader:validating field 2010-04-01 13:35 against its defined properties
INFO:filedb.loader:The field 2010-04-01 13:35 validity against its property is True
INFO:filedb.loader:The line Avengers|45|64|scheduled|2010-05-20|45.00|2010-04-01 13:35 is validated successfully against the property
INFO:filedb.loader:validated and transform the fields line
INFO:filedb.loader:validating field spiderman against its defined properties
INFO:filedb.loader:The field spiderman validity against its property is True
INFO:filedb.loader:validating field 03 against its defined properties
INFO:filedb.loader:The field 03 validity against its property is True
INFO:filedb.loader:validating field 16 against its defined properties
INFO:filedb.loader:The field 16 validity against its property is True
INFO:filedb.loader:validating field finished against its defined properties
INFO:filedb.loader:The field finished validity against its property is True
INFO:filedb.loader:validating field 2001-10-15 against its defined properties
INFO:filedb.loader:The field 2001-10-15 validity against its property is True
INFO:filedb.loader:validating field 45.00 against its defined properties
INFO:filedb.loader:The field 45.00 validity against its property is True
INFO:filedb.loader:validating field 2001-04-01 06:47 against its defined properties
INFO:filedb.loader:The field 2001-04-01 06:47 validity against its property is True
INFO:filedb.loader:The line spiderman|03|16|finished|2001-10-15|45.00|2001-04-01 06:47 is validated successfully against the property
INFO:filedb.loader:validated and transform the fields line
INFO:filedb.loader:validating field superman against its defined properties
INFO:filedb.loader:The field superman validity against its property is True
INFO:filedb.loader:validating field 42 against its defined properties
INFO:filedb.loader:The field 42 validity against its property is True
INFO:filedb.loader:validating field 128 against its defined properties
INFO:filedb.loader:The field 128 validity against its property is True
INFO:filedb.loader:validating field scheduled against its defined properties
INFO:filedb.loader:The field scheduled validity against its property is True
INFO:filedb.loader:validating field 2006-07-22 against its defined properties
INFO:filedb.loader:The field 2006-07-22 validity against its property is True
INFO:filedb.loader:validating field 25 against its defined properties
INFO:filedb.loader:The field 25 validity against its property is True
INFO:filedb.loader:validating field 2006-08-04 07:22 against its defined properties
INFO:filedb.loader:The field 2006-08-04 07:22 validity against its property is True
INFO:filedb.loader:The line superman|42|128|scheduled|2006-07-22|25|2006-08-04 07:22 is validated successfully against the property
INFO:filedb.loader:validated and transform the fields line
INFO:filedb.loader:validating field Avengers against its defined properties
INFO:filedb.loader:The field Avengers validity against its property is True
INFO:filedb.loader:validating field null against its defined properties
INFO:filedb.loader:The field null validity against its property is True
INFO:filedb.loader:validating field 32 against its defined properties
INFO:filedb.loader:The field 32 validity against its property is True
INFO:filedb.loader:validating field finished against its defined properties
INFO:filedb.loader:The field finished validity against its property is True
INFO:filedb.loader:validating field 2010-05-15 against its defined properties
INFO:filedb.loader:The field 2010-05-15 validity against its property is True
INFO:filedb.loader:validating field 22.80 against its defined properties
INFO:filedb.loader:The field 22.80 validity against its property is True
INFO:filedb.loader:validating field 2010-03-22 01:10 against its defined properties
INFO:filedb.loader:The field 2010-03-22 01:10 validity against its property is True
INFO:filedb.loader:The line Avengers|null|32|finished|2010-05-15|22.80|2010-03-22 01:10 is validated successfully against the property
INFO:filedb.loader:validated and transform the fields line
INFO:filedb.loader:validating field stealth against its defined properties
INFO:filedb.loader:The field stealth validity against its property is True
INFO:filedb.loader:validating field 42 against its defined properties
INFO:filedb.loader:The field 42 validity against its property is True
INFO:filedb.loader:validating field 128 against its defined properties
INFO:filedb.loader:The field 128 validity against its property is True
INFO:filedb.loader:validating field not required against its defined properties
INFO:filedb.loader:The field not required validity against its property is True
INFO:filedb.loader:validating field 2006-07-22 against its defined properties
INFO:filedb.loader:The field 2006-07-22 validity against its property is True
INFO:filedb.loader:validating field 35.00 against its defined properties
INFO:filedb.loader:The field 35.00 validity against its property is True
INFO:filedb.loader:validating field 2006-10-15 09:14 against its defined properties
INFO:filedb.loader:The field 2006-10-15 09:14 validity against its property is True
INFO:filedb.loader:The line stealth|42|128|not required|2006-07-22|35.00|2006-10-15 09:14 is validated successfully against the property
INFO:filedb.loader:validated and transform the fields line
INFO:filedb.loader:validating field stealth against its defined properties
INFO:filedb.loader:The field stealth validity against its property is True
INFO:filedb.loader:validating field 65 against its defined properties
INFO:filedb.loader:The field 65 validity against its property is True
INFO:filedb.loader:validating field 128 against its defined properties
INFO:filedb.loader:The field 128 validity against its property is True
INFO:filedb.loader:validating field not required against its defined properties
INFO:filedb.loader:The field not required validity against its property is True
INFO:filedb.loader:validating field 2006-07-22 against its defined properties
INFO:filedb.loader:The field 2006-07-22 validity against its property is True
INFO:filedb.loader:validating field 30.00 against its defined properties
INFO:filedb.loader:The field 30.00 validity against its property is True
INFO:filedb.loader:validating field 2006-10-15 09:14 against its defined properties
INFO:filedb.loader:The field 2006-10-15 09:14 validity against its property is True
INFO:filedb.loader:The line stealth|65|128|not required|2006-07-22|30.00|2006-10-15 09:14 is validated successfully against the property
INFO:filedb.datastore:Closing the file
```

```shell
(weta) bash-3.2$ python3 -m query
INFO:filedb.datastore:Db file already exists
PROJECT        SHOT           VERSION        STATUS         FINISH_DATE    INTERNAL_BID   CREATED_DATE
the hobbit     45             64             scheduled      2010-05-20     45.0           2010-04-01 13:35
the hobbit     null           32             finished       2010-05-15     22.8           2010-03-22 01:10
spiderman      03             16             finished       2001-10-15     45.0           2001-04-01 06:47
stealth        65             128            not required   2006-07-22     30.0           2006-10-15 09:14
king kong      42             128            not required   2006-07-22     35.0           2006-10-15 09:14
stealth        42             128            not required   2006-07-22     35.0           2006-10-15 09:14
king kong      65             128            not required   2006-07-22     30.0           2006-10-15 09:14
Avengers       null           32             finished       2010-05-15     22.8           2010-03-22 01:10
superman       42             128            scheduled      2006-07-22     25.0           2006-08-04 07:22
lotr           03             16             finished       2001-10-15     45.0           2001-04-01 06:47
Avengers       45             64             scheduled      2010-05-20     45.0           2010-04-01 13:35

```

```shell
INFO:filedb.datastore:Db file already exists
ERROR:filedb.query:cannot perform sorting aggregate function without groupby
ERROR:filedb.query:cannot perform sorting aggregate function without groupby
ERROR:filedb.query:cannot perform sorting aggregate function without groupby
ERROR:filedb.query:cannot perform sorting aggregate function without groupby
ERROR:filedb.query:cannot perform sorting aggregate function without groupby
ERROR:filedb.query:cannot perform sorting aggregate function without groupby
ERROR:filedb.query:cannot perform sorting aggregate function without groupby
ERROR:filedb.query:cannot perform sorting aggregate function without groupby
ERROR:filedb.query:cannot perform sorting aggregate function without groupby
ERROR:filedb.query:cannot perform sorting aggregate function without groupby
ERROR:filedb.query:cannot perform sorting aggregate function without groupby
PROJECT        VERSION
king kong      None
king kong      None
Avengers       None
lotr           None
spiderman      None
the hobbit     None
stealth        None
Avengers       None
stealth        None
superman       None
the hobbit     None

(weta) bash-3.2$ python3 -m query -s Project,version:count -g Project
INFO:filedb.datastore:Db file already exists
PROJECT        VERSION
Avengers       2
king kong      1
lotr           1
spiderman      1
stealth        1
superman       1
the hobbit     2
```

```shell
(weta) bash-3.2$ python3 -m query -s Project,version:count -f "PROJECT='king kong'" -g Project
INFO:filedb.datastore:Db file already exists
PROJECT        VERSION
king kong      1
```

```shell
(weta) bash-3.2$ python3 -m query -s Project,version:count -f "PROJECT='king kong' OR  PROJECT='avengers'" -g Project -o Shot
INFO:filedb.datastore:Db file already exists
PROJECT        VERSION
king kong      1
```

```shell
(weta) bash-3.2$ python3 -m query -s Project,version:count -f "PROJECT='king kong' OR  PROJECT='the hobbit'" -g Project -o Shot
INFO:filedb.datastore:Db file already exists
PROJECT        VERSION
the hobbit     2
king kong      1
```
```shell

(weta) bash-3.2$ python3 -m query -s Project,version:count,shot:collect -f "PROJECT='king kong' OR  PROJECT='the hobbit'" -g Project -o Shot
INFO:filedb.datastore:Db file already exists
PROJECT        VERSION        SHOT
king kong      1              ['65', '42']
the hobbit     2              ['null', '45']

(weta) bash-3.2$

```



