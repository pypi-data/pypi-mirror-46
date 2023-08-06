# lowhaio-retry

Wrapper that retries failed [lowhaio](https://github.com/michalc/lowhaio) HTTP requests. Allows retries of exceptions from failed HTTP requests.


## Installation

```bash
pip install lowhaio_retry
```


## Usage

The `request` function returned from `lowhaio.Pool` must be wrapped with `lowhaio_retry.retry`, as in the below example. This will retry the request, waiting the specified interval between retries. If the request still fails, the final exception will be bubbled up to client code.

So instead of a request like

```python
from lowhaio import Pool

request, _ = Pool()

body = ...

code, headers, body = await request(
    b'PUT', 'https://example.com/path', body=body,
    headers=((b'content-length', b'1234'),),
)
```

you can write

```python
from lowhaio import Pool, HttpConnectionError, HttpDataError
from lowhaio_retry import retry

request, _ = Pool()

retriable_request = retry(request,
    exception_intervals=(
        # Seconds to wait after each exception
        (HttpConnectionError, (0, 0, 0)),
        (HttpDataError, (0, 1, 2, 4)),
    ),
)

body = ...

code, headers, body = await retriable_request(
    b'PUT', 'https://example.com/path', body=body,
    headers=((b'content-length', b'1234'),),
)
```
