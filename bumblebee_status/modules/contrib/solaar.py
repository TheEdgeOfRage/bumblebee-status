"""Shows status and load percentage of logitech's unifying device

Requires the following executable:
    * solaar (from community)

contributed by `cambid <https://github.com/cambid>`_ - many thanks!
"""

import logging

import core.module
import core.widget
import core.decorators

import util.cli


class Module(core.module.Module):
    @core.decorators.every(seconds=30)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.utilization))
        self.__battery = self.parameter("device", "")
        self.background = True
        self.__battery_status = {}
        self.__error = False
        if self.__battery != "":
            self.__cmd = f"solaar show '{self.__battery}'"
        else:
            self.__cmd = "solaar show"

    @property
    def __format(self) -> str:
        return self.parameter("format", "{percent}")

    def utilization(self, widget) -> str:
        default = {
            "percent": "N/A%",
            "voltage": "N/A mV",
            "status": "N/A",
        }
        return self.__format.format(**{**default, **self.__battery_status})

    def update(self):
        self.__error = False
        code, result = util.cli.execute(
            self.__cmd, ignore_errors=True, return_exitcode=True
        )

        if code == 0:
            for line in result.split('\n'):
                if line.count('Battery') > 0:
                    res = line.split(':')[1].strip()[:-1]
                    percent, voltage, _, status = res.split(' ')
                    self.__battery_status = {
                        "percent": percent,
                        "voltage": voltage,
                        "status": status,
                    }
        else:
            self.__error = True
            logging.error(f"solaar exited with {code}: {result}")

    def state(self, widget):
        if self.__error:
            return "warning"
        return "okay"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
