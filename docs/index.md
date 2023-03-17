# Saffier

<p align="center">
  <a href="https://starlette-bridge.tarsild.io"><img src="https://res.cloudinary.com/dymmond/image/upload/v1675104815/Saffier/logo/logo_dowatx.png" alt='Saffier'></a>
</p>

<p align="center">
    <em>🚀 The only Async ORM you need. 🚀</em>
</p>

<p align="center">
<a href="https://github.com/tarsil/starlette_bridge/workflows/Test%20Suite/badge.svg?event=push&branch=main" target="_blank">
    <img src="https://github.com/tarsil/starlette_bridge/workflows/Test%20Suite/badge.svg?event=push&branch=main" alt="Test Suite">
</a>

<a href="https://pypi.org/project/starlette_bridge" target="_blank">
    <img src="https://img.shields.io/pypi/v/starlette_bridge?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

<a href="https://pypi.org/project/starlette_bridge" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/starlette_bridge.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: [https://starlette-bridge.tarsild.io](https://starlette-bridge.tarsild.io) 📚

**Source Code**: [https://github.com/tarsil/starlette_bridge](https://github.com/tarsil/starlette_bridge)

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
