# Contributing guidelines

## Code style

saltant's development has endeavoured to follow (with the exception of
detailed docstrings—which aren't conventional in Django) [Google's
Python Style
Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md),
and, where Django-specific code is concerned, [Django's coding style
guidelines](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/).

For code formatting, use [Black](https://github.com/ambv/black).

## Tests

Before submitting any non-trivial code, run tests with

```
./manage test
```

You may wish to skip over container tests, which can take awhile and in
terms of dependencies are the most demanding. To do so, simply comment
out [this
line](https://github.com/saltant-org/saltant/blob/master/tasksapi/tests/__init__.py#L4).
