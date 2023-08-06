==================
**Compare Files**
==================

Compare Files provides a way to compare latency and count products,
between two systems with incoming data. In this case, we are comparing
the arrival time of products to the ESB between legacy and enterprise.
The legacy file is downloaded via GoogleDrive and the enterprise file 
is created from querying the edpdb database. Both files are CSV.

Typical usage often looks like this::

    python database_query.py
    python compare_files.py

Prerequisites
==============
* Connection to the current host: username@nco-lw-rpotter.ncep.noaa.gov

* Python 2.7 

* Download legacy file from GoogleDrive: 
  https://drive.google.com/open?id=1dXkpZ4LxmS_6Sah7GheAnwAZmj7727Fp

* Install module psycopg2 
  http://initd.org/psycopg/

Output
-------------
1. Latency.txt
2. Legacy_Products_Count.txt
3. New_Products_Count.txt

