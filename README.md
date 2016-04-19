# csv2md

Converter CSV to Markdown's Table.
This is licensed under Apache2.

# Usgae

```hoge.csv
#Path,count
/home/hidenorly/work/python/hoge.py,2
/home/hidenorly/work/python/hoge2.py,10
```

```
$ csv2md.py hoge.csv
| Path | count |
|:---|:---|
| /home/hidenorly/work/python/hoge.py | 2 |
| /home/hidenorly/work/python/hoge2.py | 10 |
```

```
$ cat hoge.csv | csv2md.py
| Path | count |
|:---|:---|
| /home/hidenorly/work/python/hoge.py | 2 |
| /home/hidenorly/work/python/hoge2.py | 10 |
```
