# Starlette Bridge

<p align="center">
  <a href="https://starlette-bridge.tarsild.io"><img width="420px" src="https://www.starlette.io/img/starlette.png" alt='Starlette Bridge'></a>
</p>

<p align="center">
    <em>🚀 The Starlette events bridge that you need. 🚀</em>
</p>

<p align="center">
<a href="https://github.com/tarsil/starlette-bridge/workflows/Test%20Suite/badge.svg?event=push&branch=main" target="_blank">
    <img src="https://github.com/tarsil/starlette-bridge/workflows/Test%20Suite/badge.svg?event=push&branch=main" alt="Test Suite">
</a>

<a href="https://pypi.org/project/starlette-bridge" target="_blank">
    <img src="https://img.shields.io/pypi/v/starlette-bridge?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

<a href="https://pypi.org/project/starlette-bridge" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/starlette-bridge.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: [https://starlette-bridge.tarsild.io](https://starlette-bridge.tarsild.io) 📚

**Source Code**: [https://github.com/tarsil/starlette-bridge](https://github.com/tarsil/starlette-bridge)

---

## Motivation

Starlette has evolved and it will keep on growing. In the release 0.26+ it was announced the
`on_startup` and `on_shutdown` events would be removed in favour of the newly `lifepsan` and those
would be officially removed in the release 1.0.

The problem is the fact that there are a lof od packages out there still using the old ways of
using the events and this change will introduce breaking changes.

This bridge will make sure that doesn't happen and you can still use the old form of using the
`on_startup` and `on_shutdown` without breaking the `lifespan` from Starlette.

What `Starlette Bridge` does for you is simple. It gets the `on_startup` and `on_shutdown` events
in the same fashion you could do before and internally generates the newly `lifespan` for starlette.

That simple. Keeping the old syntax intact and using the newly `lifespan`.

## Installation

To install Starlette Bridge, simply run:

```shell
$ pip install starlette-bridge
```

## How to use

This is actually very simple to do it. You don't need to do anything particularly difficult, in
fact, you only need to update where your Starlette object comes from.

```python hl_lines="1"
from starlette_bridge import Starlette

app = Starlette()
```

And that is pretty much it.

### How does it work

Starlette bridge simply maps your `on_startup` and `on_shutdown` events and converts them into
the new `lifespan` async generator from `Starlette`.

This way you can continue to use your preferred way of assembling the events while maintaining
the new structure required by Starlette for managing events.

### on_event and add_event_handler

These two pieces of functionality are also supported by the bridge making sure that what you had
in the past, still remains working as is without changing the syntax.

Let us see an example how it works. We will be using [Starlette Bridge](https://saffier.tarsild.io) because
already contains events we want to use.

#### on_startup/on_shutdown

Using the `on_startup` and `on_shutdown`.

```python hl_lines="3 10-11"
from saffier import Database, Registry

from starlette_bridge import Starlette

database = Database("sqlite:///db.sqlite")
models = Registry(database=database)


app = Starlette(
    on_startup=[database.connect],
    on_shutdown=[database.disconnect],
)
```

#### Lifespan

You can, of course, use the lifespan as well.

```python hl_lines="5 20"
from contextlib import asynccontextmanager

from saffier import Database, Registry

from starlette_bridge import Starlette

database = Database("sqlite:///db.sqlite")
models = Registry(database=database)


@asynccontextmanager
async def lifespan(app: Starlette):
    # On startup
    await database.connect()
    yield
    # On shutdown
    await database.disconnect()


app = Starlette(lifespan=lifespan)
```

#### on_event and add_event_handler

As mentioned before, those two functionalities are also available.

##### on_event

```python hl_lines="3 12 17"
from saffier import Database, Registry

from starlette_bridge import Starlette

database = Database("sqlite:///db.sqlite")
models = Registry(database=database)


app = Starlette()


@app.on_event("startup")
async def start_database():
    await database.connect()


@app.on_event("shutdown")
async def close_database():
    await database.disconnect()
```

##### add_event_handler

```python hl_lines="3 10-11"
from saffier import Database, Registry

from starlette_bridge import Starlette

database = Database("sqlite:///db.sqlite")
models = Registry(database=database)


app = Starlette()
app.add_event_handler("startup", database.connect)
app.add_event_handler("shutdown", database.disconnect)
```

## Notes

This is from the same author of [Esmerald](https://esmerald.dev),
[Saffier](https://saffier.tarsild.io) and [Asyncz](https://asyncz.tarsild.io). Have a look around
those techologies as well 😄.
