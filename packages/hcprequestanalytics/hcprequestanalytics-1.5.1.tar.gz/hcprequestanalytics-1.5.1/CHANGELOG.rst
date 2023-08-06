Release History
===============

**1.5.1 2019-03-19**

*   replaced *shutil.unpack_archive* with *zipfile.Zipfile.extractall*, as *unpack_archive* seems to
    have issues with zip- file members > 2 GB.

**1.5.0 2019-01-24**

*   added a table for MAPI-related logs to the database, as well as queries
    specially tailored for MAPI

**1.4.5 2019-01-23**

*   added a query that list users accessing HCP

**1.4.4 2019-01-14**

*   added some more queries

**1.4.3 2019-01-13**

*   removed unnecessary debug output

**1.4.2 2019-01-11**

*   added queries related to Tenant / Namespace / protocol

**1.4.1 2019-01-04**

*   very minor optical changes to the result XLSX file (index sheet)

**1.4.0 2018-12-27**

*   made compatibility changes for log packages created by HCP 8.x

**1.3.8 2017-12-07**

*   fixed a bug that caused log packages to fail if they contained HCP-S logs
*   Fixed a bug that caused a crash in analyze when a query didn't return any
    data
*   made using *setproctitle* optional when installing through pip for
    environments that are not supported (CygWin, for example)

**1.3.7 2017-12-07**

*   fixed setup.py to include pre-requisite *setproctitle*
    (thanks to Kevin, again)

**1.3.6 2017-11-01**

*   now properly builds with Python 3.6.3 and PyInstaller 3.3; removed the note
    from docs

**1.3.5 2017-10-30**

*   now using *setproctitle* to set more clear process titles (for ps, htop)

**1.3.4 2017-10-13**

*   fixed a bug invented in 1.3.3 that caused long running queries to break
    xlsx creation (thanks to Kevin Varley for uncovering this)

**1.3.3 2017-10-12**

*   removed gridlines from the content sheet
*   fine-tuned the column width in the query sheets
*   made the runtime column a bit more readable
*   added *500_largest_size* query
*   some documentation additions

**1.3.2 2017-10-10**

*   added query runtime to content sheet in xlsx

**1.3.1 2017-10-05**

*   added timestamp of first and last record to xlsx file
*   added SQL function ``tp(size, latency)`` to calculate the throughput
*   adopted queries to use ``tp()``

**1.3.0 2017-10-03**

*   some more xlsx luxury
*   added more queries
*   added the ability to dump the built-in queries to stdout
*   re-worked the cmd-line parameters (-d is now where it belongs to...)

**1.2.2 2017-09-26**

*   documentation fixes

**1.2.1 2017-09-25**

*   removed percentile() from the most queries, due to too long runtime on
    huge datasets
*   added the possibility to select a group of queries on *analyze*

**1.2.0 2017-09-24**

*   now analyze runs up to cpu_count subprocesses, which will run the queries
    in parallel
*   added cmdline parameter ``--procs`` to allow to set the no. of
    subprocesses to use, bypassing the cpu_count

**1.1.1 2017-09-23**

*   added per-day queries
*   all numerical fields in the XLSX file now formated as #.##0

**1.1.0 2017-09-23**

*   re-built the mechanism to add individual queries
*   \*.spec file prepared to build with pyinstaller w/o change on macOS and
    Linux

**1.0.4 2017-09-22**

*   a little more featured XLXS files

**1.0.3 2017-09-21**

*   now creating a single XLSX file on *analyze*, added option -c to create
    CSV files instead

**1.0.2 2017-09-16**

*   fixed the timestamp column (now hold the seconds since Epoch)

**1.0.1 2017-09-15**

*   now we do understand log records of access to the Default Namespace properly
*   speed-up of unpacking by just unpacking the required archives

**1.0.0 2017-09-10**

*   initial release
