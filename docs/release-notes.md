# Release Notes

## 0.3.0

### Updated

- Added the latest version of starlette to 0.28.0.

## 0.2.0

### Fixed

- Upgrade Starlette version to >=0.27.0 for a security release. Details on [Starlette's security](https://github.com/encode/starlette/security/advisories/GHSA-v5gw-mw7f-84px)

## 0.1.0

This is the initial release of Starlette Bridge.

* Simple bridge allowing to keep individual `on_startup`/`on_shutdown` events even those
where depracated by `Starlette`. 
* `on_event` and `add_event_handler` available to be used like Starlette.
