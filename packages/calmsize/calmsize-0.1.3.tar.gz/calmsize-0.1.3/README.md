calmsize
==============
[![Build Status](https://travis-ci.com/Stonesjtu/calmsize.svg?token=vyTdxHbi1PCRzV6disHp&branch=master)](https://travis-ci.com/Stonesjtu/calmsize)
![PyPI](https://img.shields.io/pypi/v/calmsize.svg)
[![PyPI download month](https://img.shields.io/pypi/dm/calmsize.svg)](https://pypi.python.org/pypi/calmsize/)


### NOTICE

I forked the repo from source file downloaded from pip `hurry.filesize`.
That simple library is very useful when debugging memory issues, but 
unfortunately out-of-maintainance since 2009, so I decided to fork
the great work of Martijn Faassen, Startifact.

### Intro

calmsize a simple Python library that can take a number of bytes and
returns a human-readable string with the size in it, in kilobytes (K),
megabytes (M), etc.

The default system it uses is "traditional", where multipliers of 1024
increase the unit size::

```ipython
>>> from calmsize import size, ByteSize
>>> size(1024)
'1K'
>>> size(-1024)
'-1K'
>>> '{:.2f}'.format(size(-1024))
'-1.00K'
```

An alternative, slightly more verbose system::

```ipython
>>> from calmsize import alternative
>>> size(1, system=alternative)
'1 byte'
>>> size(10, system=alternative)
'10 bytes'
>>> size(1024, system=alternative)
'1 KB'
```

A verbose system::

```ipython
>>> from calmsize import verbose
>>> size(10, system=verbose)
'10 bytes'
>>> size(1024, system=verbose)
'1 kilobyte'
>>> size(2000, system=verbose)
'1 kilobyte'
>>> size(3000, system=verbose)
'2 kilobytes'
>>> size(1024 * 1024, system=verbose)
'1 megabyte'
>>> size(1024 * 1024 * 3, system=verbose)
'3 megabytes'
```

You can also use the SI system, where multipliers of 1000 increase the unit
size::

```ipython
>>> from calmsize import si
>>> size(1000, system=si)
'1K'
```
