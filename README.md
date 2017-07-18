httpclient2
===========

original http client

## Requirement

### Python

Python3

### HTTP library

[Requests](http://docs.python-requests.org/en/master/#)


#### How to install 'requests'

$pip install requests

## Usage

### client.py

```
$python client.py [URL] [NUM]
```

This 'NUM' means 'num of TCP connections'.

Each TCP connection has one HTTP request.

### client2.py

```
$python client2.py [URL] [NUM]
```

This 'NUM' means 'num of HTTP requests per connection'.

This client has only one TCP connection.

### test.sh
Request sample movie file and play using VLC

```
$./test.sh [NUM_OF_CONNECTION] [SLEEP_TIME(sec)]
```
