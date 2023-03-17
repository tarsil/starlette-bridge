import typing

from starlette.applications import Starlette as BaseStarlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute
from starlette.types import Lifespan

from starlette_bridge.routing import BridgeRouter

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
        redirect_slashes: bool = True,
    ) -> None:
        super().__init__(
            debug=debug,
            routes=routes,
            middleware=middleware,
            exception_handlers=exception_handlers,
            lifespan=lifespan,
        )

        # Apply the Bridge router
        self.router = BridgeRouter(
            routes=routes,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            redirect_slashes=redirect_slashes,
        )

    def on_event(self, event_type: str) -> typing.Callable:  # pragma: nocover
        """
        Add an event on_startup and on_shutdown with Esmerald underlying
        implementation of the lifespan.
        """
        return self.router.on_event(event_type)

    def add_event_handler(
        self, event_type: str, func: typing.Callable
    ) -> None:  # pragma: no cover
        self.router.add_event_handler(event_type, func)
