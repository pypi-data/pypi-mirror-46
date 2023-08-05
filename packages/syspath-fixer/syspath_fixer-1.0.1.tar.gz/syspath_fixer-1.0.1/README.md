# syspath-fixer #

- Are you tired of getting ImportErrors when building multi-module applications in Python?  
- Are you tired of endlessly appending modules to `sys.path`?  

Here comes syspath_fixer!
Simply:
```bash
pip install syspath-fixer
```
```python
__import__('syspath_fixer').fix(__file__)
```
And all your pain will be gone!

Syspath-fixer recursively adds python modules to the `sys.path`, so you don't have to.
