# Contributing guidelines

## Code style

saltant's development has endeavoured to follow (with the exception of
detailed docstrings—which aren't conventional in Django) [Google's
Python Style
Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md),
and, where Django-specific code is concerned, [Django's coding style
guidelines](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/).

1. Copying the style of existing code should be enough, but when that's
   not enough, consult the above style guides.
2. [Lint](https://www.pylint.org/) your code before requesting to pull
   in code. Pylint doesn't exactly play nice with Django code, so it
   takes a bit of experience to determine which complaints are valid and
   which aren't (also see the Pylint Django plugin
   [pylint-django](https://github.com/PyCQA/pylint-django), which can
   help with this).

## Tests

Before submitting any non-trivial code, run tests with

```
./manage test
```

You may wish to skip over container tests, which can take awhile and in
terms of dependencies are the most demanding. To do so, simply comment
out [this
line](https://github.com/mwiens91/saltant/blob/master/tasksapi/tests/__init__.py#L4).
