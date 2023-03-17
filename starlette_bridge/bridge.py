import typing

from starlette.applications import Starlette as BaseStarlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute
from starlette.types import Lifespan

from starlette_bridge.context_managers import AyncLifespanContextManager

AppType = typing.TypeVar("AppType", bound="Starlette")


class Starlette(BaseStarlette):
    """Same object representation of Starlette. It does exactly the same as Starlette, literally, and bridges the events.

    Creates an application instance.
    """

    def __init__(
        self: "AppType",
        debug: bool = False,
        routes: typing.Optional[typing.Sequence[BaseRoute]] = None,
        middleware: typing.Optional[typing.Sequence[Middleware]] = None,
        exception_handlers: typing.Optional[
            typing.Mapping[
                typing.Any,
                typing.Callable[
                    [Request, Exception],
                    typing.Union[Response, typing.Awaitable[Response]],
                ],
            ]
        ] = None,
        on_startup: typing.Optional[typing.Sequence[typing.Callable]] = None,
        on_shutdown: typing.Optional[typing.Sequence[typing.Callable]] = None,
        lifespan: typing.Optional[Lifespan["AppType"]] = None,
    ) -> None:
        assert lifespan is None or (
            on_startup is None and on_shutdown is None
        ), "Use either 'lifespan' or 'on_startup'/'on_shutdown', not both."

        self.lifespan = self.handle_lifespan_events(
            on_startup=on_startup, on_shutdown=on_shutdown, lifespan=lifespan
        )

        super().__init__(
            debug=debug,
            routes=routes,
            middleware=middleware,
            exception_handlers=exception_handlers,
            lifespan=self.lifespan,
        )

    def handle_lifespan_events(
        self,
        on_startup: typing.Optional[typing.Sequence[typing.Callable]] = None,
        on_shutdown: typing.Optional[typing.Sequence[typing.Callable]] = None,
        lifespan: typing.Optional[Lifespan["AppType"]] = None,
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

    def on_event(self, event_type: str) -> typing.Callable:  # pragma: nocover
        return self.router.on_event(event_type)

    def add_event_handler(
        self, event_type: str, func: typing.Callable
    ) -> None:  # pragma: no cover
        self.router.add_event_handler(event_type, func)
