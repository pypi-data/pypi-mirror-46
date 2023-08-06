# tox-backticks

tox-backticks allows use of backticks within `setenv` to run commands
to populate environment variables that can then be accessed using `{env:var}`.

```ini
[testenv:simple]
setenv =
  FOO=`python -c 'import sys; sys.stdout.write("foo")'`
commands =
  python -c 'assert "{env:FOO}" == "foo"'
```

Commands within the backticks follow the standard tox rules, where
it must be an executable installed into the venv, or be an executable
permitted using `whitelist_externals`.

To reduce the impact on the tox syntax, the backticks must enclose the
entire setenv line.  Due to this choice, this plugin will only break
existing tox usage where a user wanted an environment variable which
started and ended with a literal backtick, deemed rather unlikely
and judged to be foolish anyway.  If that is truely needed, the following
approach allows literal backticks at start and end.

[testenv:literal_ignored]
setenv =
  BACKTICK=`
  INNERBACKTICK=``{env:BACKTICK}
commands =
  python -c 'assert "{env:INNERBACKTICKS}" == "```"'

To use backticks for a part of a variable, use multiple setenv.
The order of setenv is irrelevant.

```ini
[testenv:nested_reversed]
setenv =
  BAR=`{env:FOO} -c 'import sys; sys.stdout.write("foo")'`
  FOO=`python -c 'import sys; sys.stdout.write("python")'`
commands =
  python -c 'assert "{env:BAR}" == "foo"'
```

Tox will report an error if multiple setenv are recursively defined,
preventing the correct order from being established.

See [`tests/tox.ini`](tests/tox.ini) for samples.

