import wandb
from wandb.apis import InternalApi
from wandb.run_manager import RunManager
import time
import os
import threading
import uuid
from IPython.core.getipython import get_ipython
from IPython.core.magic import cell_magic, line_cell_magic, line_magic, Magics, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import display, Javascript
from pkg_resources import resource_filename
from importlib import import_module


@magics_class
class WandBMagics(Magics):
    def __init__(self, shell, require_interaction=False):
        super(WandBMagics, self).__init__(shell)
        self.options = {}

    @magic_arguments()
    @argument(
        "-d", "--display", default=True,
        help="Display the wandb interface automatically"
    )
    @line_cell_magic
    def wandb(self, line, cell=None):
        # Record options
        args = parse_argstring(self.wandb, line)
        self.options["body"] = ""
        self.options['wandb_display'] = args.display

        # Register events
        display(Run())
        if cell is not None:
            get_ipython().run_cell(cell)


class JupyterAgent(object):
    """A class that only logs metrics after `wandb.log` has been called and stops logging at cell completion"""

    def __init__(self):
        self.paused = True

    def start(self):
        if self.paused:
            self.api = InternalApi()
            self.rm = RunManager(self.api, wandb.run, output=False)
            self.api._file_stream_api = None
            self.api.set_current_run_id(wandb.run.id)
            self.rm.mirror_stdout_stderr()
            self.paused = False
            # Init will return the last step of a resumed run
            # we update the runs history._steps in extreme hack fashion
            # TODO: this reserves a bigtime refactor
            new_step = self.rm.init_run(dict(os.environ))
            if new_step:
                wandb.run.history._steps = new_step + 1

    def stop(self):
        if not self.paused:
            self.rm.unmirror_stdout_stderr()
            self.rm.shutdown()
            wandb.run.close_files()
            self.paused = True


class Run(object):
    def __init__(self, run=None):
        self.run = run or wandb.run

    def _repr_html_(self):
        state = "running"
        if self.run._jupyter_agent == None:
            state = "no_agent"
        elif self.run._jupyter_agent.paused:
            state = "paused"
        url = self.run.get_url() + "?jupyter=true&state=" + state
        return '''<iframe src="%s" style="border:none;width:100%%;height:420px">
        </iframe>''' % url
