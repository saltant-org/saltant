# Contributing

## Code style

saltant's development has endeavoured to follow (with the exception of
detailed docstrings—which aren't conventional in Django) [Google's
Python Style
Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md),
and, where Django-specific code is concerned, [Django's coding style
guidelines](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/).

For code formatting, use [Black](https://github.com/ambv/black).

```
black .
```

is the command you want to run from the repository root.

## Tests

Before submitting any non-trivial code, run tests with

```
./manage.py test
```

You may wish to skip over the execution tests, since these can leave
behind files that can only be removed with root (see the corresponding
issue at https://github.com/saltant-org/saltant/issues/4a).

Also consider *writing* tests when adding non-trivial features. At the
very least, please least write a TODO reminder somewhere that tests
should be written.  If you want to write tests but have questions, ask
[@mwiens91](https://github.com/mwiens91).

### Travis CI

When you submit or make changes to a pull request, Travis CI will run
its builds. For whatever reason, Travis frequently errors with this
project, so if it reports an error, check the logs and make sure it's
not just a bug on the builds' end!

## Seeding a fresh database

saltant comes with a data fixture that's used internally for its tests,
which can also be used to seed a fresh database. If you'd like to do so,
run

```
./manage.py loaddata test-fixture.yaml
```
