# Example Usage

The usage of this API is through REST endpoint `/getid`.

## The API

Get a range of unique IDs for a given mode.

```
$ curl 'http://localhost:8051/getid?range=10&mode=file'
{"endIndex": 9, "startIndex": 0}
```

Select a different mode to get different unique IDs. If a mode is
currently unsupported by the database, a new row will be started to
support it.

```
$ curl 'http://localhost:8000/getid?range=10&mode=file'
{"endIndex": 9, "startIndex": 0}
$ curl 'http://localhost:8000/getid?range=10&mode=upload'
{"endIndex": 9, "startIndex": 0}
```
