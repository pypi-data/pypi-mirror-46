import json
import os

from IPython.utils.tempdir     import TemporaryDirectory
from jupyter_client.kernelspec import KernelSpecManager

class Kernel_Install_Inside_Jupyter:

    def __init__(self, kernel_class,kernel_name, kernel_spec=None):
        self.kernel_module = kernel_class.__module__
        self.kernel_name   = kernel_name
        self.kernel_spec   = kernel_spec

    def install(self):
        with TemporaryDirectory() as td:
            os.chmod(td, 0o755) # check if this is needed
            with open(os.path.join(td, 'kernel.json'), 'w') as file:
                json.dump(self.kernel_spec, file, sort_keys=True)
            return KernelSpecManager().install_kernel_spec(td, self.kernel_name, replace=True)

    def uninstall(self):
        return KernelSpecManager().remove_kernel_spec(self.kernel_name.lower())


class Kernel_Install:

    def __init__(self, kernel_name, kernel_class, kernel_spec, jupyter_kernel):
        self.kernel_name    = kernel_name
        self.kernel_class   = kernel_class.__name__
        self.kernel_module  = kernel_class.__module__
        self.kernel_spec    = kernel_spec
        self.jupyter_kernel = jupyter_kernel

        self.install_code   = """   
                                   from {0} import {1}
                                   from osbot_jupyter.api.Kernel_Install import Kernel_Install_Inside_Jupyter                                                       
                                   Kernel_Install_Inside_Jupyter({1},'{2}',{3}).install()                                   
                              """.format(self.kernel_module, self.kernel_class, self.kernel_name, json.dumps(self.kernel_spec))
        self.uninstall_code = """
                                   from {0} import {1}
                                   from osbot_jupyter.api.Kernel_Install import Kernel_Install_Inside_Jupyter                    
                                   Kernel_Install_Inside_Jupyter({1},'{2}').uninstall()
                              """.format(self.kernel_module, self.kernel_class, self.kernel_name)

    def current_kernels(self):
        return self.jupyter_kernel.kernels_specs()

    def exists(self):
        return self.kernel_name.lower() in set(self.current_kernels())

    def install(self):
        return self.jupyter_kernel.execute(self.install_code)

    def uninstall(self):
        if self.exists():
            return self.jupyter_kernel.execute(self.uninstall_code)
        return None


