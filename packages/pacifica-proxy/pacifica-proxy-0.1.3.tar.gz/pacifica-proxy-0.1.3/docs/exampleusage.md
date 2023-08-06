# Example Usage

Different paths in the Proxy service have different usages. The files API
is currently only provided but future paths could be added.

## Files Access

The [archive interface service](https://github.com/pacifica/pacifica-archiveinterface)
is intended to be used by internal services to access files off the archive by
file ID only. This can be easily iterated over by external users and should not
be exposed externally. This service accepts a hashsum provided by the user and
looks up a file ID based on that hashsum. The service then redirects the request
without knowledge of the user to the archive interface to pull the file.

### File Access API

Example curl command
```
curl http://localhost:8180/files/sha1/f90a581a5099079a8f1f582dd3643b6e060cc551
```

If the file exists the file is given as an octet-stream to the user. The
disposition header is also set with the filename defined in the metadata for
that file.

If the file does not exist a `404 Not Found` return code is given.
