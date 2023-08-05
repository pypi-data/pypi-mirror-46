# Example Usage

## Verify working

To verify the system is working do a GET against the system with no id specified.
```
curl -X GET http://127.0.0.1:8080
```

Sample output:
```
{
    "message": "Pacifica Archive Interface Up and Running"
}
```

## Put a File

The path in the URL should be only an integer specifying a unique
file in the archive. Sending a different file to the same URL will
over-write the contents of the previous file. Setting the Last-
Modified header sets the mtime of the file in the archive and is
required.

```
curl -X PUT -H 'Last-Modified: Sun, 06 Nov 1994 08:49:37 GMT' --upload-file /tmp/foo.txt http://127.0.0.1:8080/12345
```

Sample output:
```
{
    "message": "File added to archive",
    "total_bytes": "24"
}
```

## Get a File
The HTTP `GET` method is used to get the contents
of the specified file.
```
curl -o /tmp/foo.txt http://127.0.0.1:8080/12345
```
Sample output (without -o option):
"Document Contents"

## Status a File

The HTTP ```HEAD``` method is used to get a JSON document describing the
status of the file. The status includes, but is not limited to, the
size, mtime, ctime, whether its on disk or tape. The values can be found
within the headers.
```
curl -I -X HEAD http://127.0.0.1:8080/12345
```
Sample output:
```
HTTP/1.0 204 No Content
Date: Fri, 07 Oct 2016 19:51:37 GMT
Server: WSGIServer/0.1 Python/2.7.5
X-Pacifica-Messsage: File was found
X-Pacifica-File: /tmp/12345
Content-Length: 18
Last-Modified: 1473806059.29
X-Pacifica-Ctime: 1473806059.29
X-Pacifica-Bytes-Per-Level: (18L,)
X-Pacifica-File-Storage-Media: disk
Content-Type: application/json

```

## Stage a File
The HTTP `POST` method is used to stage a file for use.  In posix this
equates to a no-op on hpss it stages the file to the disk drive.

```
curl -X POST -d '' http://127.0.0.1:8080/12345
```

Sample Output:
```
{
    "file": "/12345",
    "message": "File was staged"
}
```

## Move a File
The HTTP `PATCH` method is used to move a file.
The upload file contains the path to current file on archive
The Id at the end of the url is where the file will be moved to

```
curl -X PATCH -H 'Content-Type: application/json' http://127.0.0.1:8080/123456 -d'{
  "path": "/tmp/12345"
}'
```

Sample Output:
```
{
    "message": "File Moved Successfully"
}
```
