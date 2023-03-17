import typing

from starlette.routing import BaseRoute
from starlette.routing import Router as Router
from starlette.types import ASGIApp, Lifespan

from starlette_bridge.context_managers import AyncLifespanContextManager


class BridgeRouter(Router):
    def __init__(
        self,
        routes: typing.Optional[typing.Sequence[BaseRoute]] = None,
        redirect_slashes: bool = True,
        default: typing.Optional[ASGIApp] = None,
        on_startup: typing.Optional[typing.Sequence[typing.Callable]] = None,
        on_shutdown: typing.Optional[typing.Sequence[typing.Callable]] = None,
        lifespan: typing.Optional[Lifespan[typing.Any]] = None,
    ) -> None:
        assert lifespan is None or (
            on_startup is None and on_shutdown is None
        ), "Use either 'lifespan' or 'on_startup'/'on_shutdown', not both."

        self.lifespan_bridge: typing.Any = self.handle_lifespan_events(
            on_startup=on_startup, on_shutdown=on_shutdown, lifespan=lifespan
        )
        super().__init__(
            routes=routes,
            redirect_slashes=redirect_slashes,
            default=default,
            lifespan=lifespan,
        )

        self.on_startup = [] if on_startup is None else list(on_startup)
        self.on_shutdown = [] if on_shutdown is None else list(on_shutdown)

    def handle_lifespan_events(
        self,
        on_startup: typing.Optional[typing.Sequence[typing.Callable]] = None,
        on_shutdown: typing.Optional[typing.Sequence[typing.Callable]] = None,
        lifespan: typing.Optional[Lifespan[typing.Any]] = None,
    ) -> typing.Any:
        """Handles with the lifespan events in the new Starlette format of lifespan.
        This adds a mask that keeps the old `on_startup` and `on_shutdown` events variable
        declaration for legacy and comprehension purposes and build the async context manager
        for the lifespan.
        """
        if on_startup or on_shutdown:
            return AyncLifespanContextManager(on_startup=on_startup, on_shutdown=on_shutdown)
        elif lifespan:
            return lifespan
        return None

    def add_event_handler(
        self, event_type: str, func: typing.Callable
    ) -> None:  # pragma: no cover
        assert event_type in ("startup", "shutdown")

        if event_type == "startup":
            self.on_startup.append(func)

        else:
            self.on_shutdown.append(func)

    def on_event(self, event_type: str) -> typing.Callable:  # pragma: no cover
        def decorator(func: typing.Callable) -> typing.Callable:
            self.add_event_handler(event_type, func)
            return func

        return decorator
