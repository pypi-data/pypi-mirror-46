## Usage
```py
import pathing

root = (
    {
        0: {
            'some': [
                'data',
                'right'
            ],
            'here': True
        },
        'is': {
            False: 'too',
            'deep': {
                'for': {
                    'this': {
                        'depth': 'level'
                    }
                },
                'but': {
                    'here': 'it is just right'
                }
            }
        }
    }
)

for keys, value in pathing.derive(root, max = 4):

    print(keys, '->', value)
```
## Installing
```
python3 -m pip install pathing
```
