# Logquicky

## Nicer python logging in one line

The python logging package from the standard library is awesome and its certainly much better than sprinkling `print()` statement all over your code.
However, even hough setting it up takes just a few lines of code, configuring it to make it look nice across projects, just adds up to doing the same thing over and over.

Therefore, I created *logquicky*.

Because this is basically just a very simple configuration on the logging module, which also makes it very easy to fall back to it once you decide your project needs more advanced functionalities.
However, it hopes to save you some time when quickly building scripts or when getting started in a new project.

Finally, this is also my first (hopefully useful) little OpenSource contribution up on PyPI, so I figured it would be a good exercise.

## Features

- Colored log levels make it easy to identify different levels.
- Pre-configured formatting of log lines,
- Optional logging to a log file,
- Ability to rewrite lines for nicer progress bars etc.
- Based on Python's logging module.

## Installation

```bash
pip install logquicky
```

### Notes

logquicky is supported for python 3.6+ (due to usage of f-strings)

## How to use

### Basic example

```python
import logquicky

# Add this line to create your logger.
log = logquicky.create('my-logger')

# Start logging!
log.info("This is a log message")
```

### See how it looks in action

![simple.svg](examples/example.svg)

### Logging from multiple files

```python
#!/usr/bin/env python
# --- example2.py ---
import logquicky
import other_file

# Creates a new logger and returns it.
log = logquicky.create('my-logger')

log.info("I can log from here...")
```

```python
# --- example2_other_file.py ---
import logquicky

log = logquicky.load('my-logger')

def run():
  log.info("And from here as well!")
```

Result:

```bash
2019-02-28 12:16:56 my-logger [INFO] I can log from here...
2019-02-28 12:16:56 my-logger [INFO] And from here as well!
```