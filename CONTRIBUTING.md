# Contributing

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
./manage.py test
```

You may wish to skip over the execution tests, since these can leave
behind files that can only be removed with root (see the corresponding
issue at https://github.com/saltant-org/saltant/issues/4a).

### Travis CI

When you submit or make changes to a pull request, Travis CI will run.
For whatever reason, Travis frequently errors with this project, so if
it reports errors, check the logs and make sure it's not just a bug on
the build's end!

## Seed data

saltant comes with some data that's used internally for its tests, but
you can also use it to seed your database. If you'd like to do so, run

```
./manage.py loaddata test-fixture.yaml
```
