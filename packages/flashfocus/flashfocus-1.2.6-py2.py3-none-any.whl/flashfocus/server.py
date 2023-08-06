"""Flash windows on focus."""
from __future__ import division

import logging

try:
    from queue import Empty, Queue
except ImportError:
    from Queue import Empty, Queue
from signal import default_int_handler, SIGINT, signal

from xcffib.xproto import WindowError
import xpybutil
import xpybutil.window

from flashfocus.producer import ClientMonitor, XHandler
from flashfocus.router import FlashRouter, UnexpectedRequestType
from flashfocus.xutil import list_mapped_windows, unset_all_window_opacity, WMError


# Ensure that SIGINTs are handled correctly
signal(SIGINT, default_int_handler)


class FlashServer:
    """Handle focus shifts and client (flash_window) requests.

    Parameters
    ----------
    flash_opacity: float (between 0 and 1)
        Flash opacity.
    default_opacity: float (between 0 and 1)
        Windows are restored to this opacity post-flash.
    time: float > 0
        Flash interval in milliseconds.
    ntimepoints: int
        Number of timepoints in the flash animation. Higher values will lead to
        smoother animations at the cost of increased X server requests.
        Ignored if simple is True.
    simple: bool
        If True, don't animate flashes. Setting this parameter improves
        performance but opacity transitions are less smooth.
    flash_on_focus: bool
        If True, windows will be flashed on focus. Otherwise, windows will only
        be flashed on request.
    flash_lone_windows: str
        One of 'never', 'always', 'on_switch', 'on_open_close'

    Attributes
    ----------
    router: FlashRouter
        Object used to match window id's to flash parameters from the config
        file.
    keep_going: bool
        Setting this to False terminates the event loop (but does not initiate
        cleanup).
    producers: List[Thread]
        List of threads which produce work for the server.
    flash_requests: Queue
        Queue of flash jobs for the server to work through. Each item of the
        queue is a tuple of (window id, request type).

    """

    def __init__(
        self,
        default_opacity,
        flash_opacity,
        time,
        ntimepoints,
        simple,
        rules,
        flash_on_focus,
        flash_lone_windows,
    ):
        self.router = FlashRouter(
            defaults={
                "default_opacity": default_opacity,
                "flash_opacity": flash_opacity,
                "simple": simple,
                "rules": rules,
                "time": time,
                "ntimepoints": ntimepoints,
                "flash_on_focus": flash_on_focus,
                "flash_lone_windows": flash_lone_windows,
            },
            config_rules=rules,
        )
        self.flash_requests = Queue()
        self.producers = [ClientMonitor(self.flash_requests), XHandler(self.flash_requests)]
        self.keep_going = True

    def event_loop(self):
        """Wait for changes in focus or client requests and queues flashes."""
        self._set_all_window_opacity_to_default()
        try:
            for producer in self.producers:
                producer.start()
            while self.keep_going:
                self._flash_queued_window()
        except (KeyboardInterrupt, SystemExit):
            logging.warn("Interrupt received, shutting down...")
            self.shutdown()

    def shutdown(self, disconnect_from_xorg=True):
        """Cleanup after recieving a SIGINT."""
        self.keep_going = False
        self._kill_producers()
        logging.info("Resetting windows to full opacity...")
        unset_all_window_opacity()
        if disconnect_from_xorg:
            logging.info("Disconnecting from X session...")
            xpybutil.conn.disconnect()

    def _flash_queued_window(self):
        """Pop a window from the flash_requests queue and initiate flash."""
        try:
            window, request_type = self.flash_requests.get(timeout=1)
        except Empty:
            return None

        try:
            self.router.route_request(window, request_type)
        except UnexpectedRequestType:
            logging.error("Unexpected request type - {}. Aborting...".format(request_type))
            self.shutdown()
        except (WindowError, WMError):
            pass

    def _kill_producers(self):
        logging.info("Terminating threads...")
        for producer in self.producers:
            producer.stop()

    def _set_all_window_opacity_to_default(self):
        logging.info("Setting all windows to their default opacity...")
        for window in list_mapped_windows():
            self.router.route_request(window, "window_init")
