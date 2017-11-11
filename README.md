# Egg

A file server without data storage.

## What and Why

Egg is a file server with no awareness or data about its content. Because Egg uses UUIDs as identifiers for each file multiply applications can use the same instance which helps altering the context of the files even more.

## Setup

```bash
git clone https://github.com/Abbe98/egg.git
cd egg
```

Update the `key` variable in `egg/app.py`, this value will be your API key.

```
pipenv install
pipenv run python3 egg/app.py
```

## Usage

If anything fails or you try using a method or URL not supported Egg will only return 404 responses.

### Authentication

Set the `X-Api-Key` header to the specified API key.

### Uploading

Uploading is done with a HTTP POST request(multipart/form-data) to the root URL(`/`). See raw a raw HTML example in the examples directory. If the request is successful an UUID will be returned in the response body.

### Retrieving

Retrieving a file is done with a GET request to root following the pattern: `/<uuid>`.

### Deleting

Deleting a file is done by sending a `DELETE` request to `/<uuid>`.


## Notes

Egg is at this stage not suitable for large amounts of files. Because Egg is not aware of it's content it has to loop through filenames to match an UUID to the right one this can cause performance issues.
