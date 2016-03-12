# aiofirebase


asyncio (PEP 3156) Firebase client library.

## Usage

### Setup

Begin by importing aiofirebase:

```python
>>> import aiofirebase
```

And create a client that we will use to interact with firebase:

```python
>>> firebase = aiofirebase.Firebase("https://<YOUR-FIREBASE-APP>.firebaseio.com/")
```

### Retrieving data

We can now read data from our database:

```python
>>> firebase.read('dinosaurs')
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
>>> firebase.create('dinosaurs', {'stegosaurus': {'height': 4, 'length': 9, 'weight': 2500}}
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
>>> firebase.update('dinosaurs/stegosaurus', {'width': 2}
{
  "width": 2
}
```

*Note: If we had done a `create` instead of a `update`, the data we added in the `create` would of been overwritten.*

We can also update values at multiple locations in your Firebase database at the same time:

```python
>>> firebase.update('dinosaurs', {'lambeosaurus/width': 1, 'stegosaurus/width': 2})
```
