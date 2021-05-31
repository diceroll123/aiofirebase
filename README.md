# aiofirebase

[![PyPI version](https://badge.fury.io/py/aiofirebase.svg)](https://badge.fury.io/py/aiofirebase)

asyncio (PEP 3156) Firebase client library.

## Install

aiofirebase requires Python 3.5 or above.

```bash
$ pip install aiofirebase
```

_for this fork of mine:_

```bash
$ python -m pip install -U git+https://github.com/diceroll123/aiofirebase
```

## Usage

### Setup

Begin by importing aiofirebase:

```python
>>> import aiofirebase
```

And create a client that we will use to interact with firebase:

```python
>>> firebase = aiofirebase.FirebaseHTTP("https://<YOUR-FIREBASE-APP>.firebaseio.com/")
```

### Retrieving data

We can now read data from our database:

```python
>>> await firebase.get(path='dinosaurs')
"dinosaurs": {
  "lambeosaurus": {
    "height": 2.1,
    "length": 12.5,
    "weight": 5000
  }
}
```

### Saving data

We can also create new data in the database:

```python
>>> await firebase.put(path='dinosaurs', value={'stegosaurus': {'height': 4, 'length': 9, 'weight': 2500}})
{
  'stegosaurus': {
    "height": 4,
    "length": 9,
    "weight: 2500
  }
}
```

### Update data

We can also update specific children at a location without overwriting existing data:

```python
>>> await firebase.patch(path='dinosaurs/stegosaurus', value={'width': 2})
{
  "width": 2
}
```

*Note: If we had done a `create` instead of a `update`, the data we added in the `create` would of been overwritten.*

We can also update values at multiple locations in your Firebase database at the same time:

```python
>>> await firebase.patch(path='dinosaurs', value={'lambeosaurus/width': 1, 'stegosaurus/width': 2})
```

### Saving lists of data

If you need to save lists of data, each item should be saved against a unique key. Firebase will generate this unique
key and save the child by making a POST request.

```python
>>> await firebase.post(path='posts', value={'author': 'alanisawesome', 'title': 'The Turing Machine'})
```

### Removing data

Data can also be removed by making a DELETE request:

```python
>>> await firebase.delete('dinosaurs/stegosaurus')
```

### Watch for updates

Firebase provides a way to receive events when data changes in your database via the EventSource protocol.

aiofirebase can listen for these events, and send each event received to a callback of your choice.

```python
>>> async def mycallback(event, data):
...     print('{} event received.'.format(event))
...
>>> await firebase.stream(callback=mycallback, path='dinosaurs')
```
