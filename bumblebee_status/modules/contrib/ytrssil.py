"""Show number of new yt videos.

Requires the following library:
    * ytrssil (from aur)

contributed by `Pavle Portic <>`_ - many thanks!
"""

import logging

from ytrssil.api import get_new_video_count

import core.module
import core.widget
import core.decorators


class Module(core.module.Module):
    @core.decorators.every(minutes=30)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.utilization))
        self.background = True
        self.__videos = 0
        self.__error = False

    @property
    def __format(self):
        return self.parameter("format", "{}")

    def utilization(self, widget):
        return self.__format.format(self.__videos)

    def hidden(self):
        return self.__videos == 0 and not self.__error

    def update(self):
        self.__error = False

        try:
            self.__videos = get_new_video_count()
        except Exception as e:
            logging.error("ytrssil error: {}".format(e))
            self.__error = True

    def state(self, widget):
        if self.__error:
            return "critical"

        return ""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
