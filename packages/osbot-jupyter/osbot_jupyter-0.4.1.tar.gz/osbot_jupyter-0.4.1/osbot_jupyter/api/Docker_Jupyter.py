import docker
from pbx_gs_python_utils.utils.Dev import Dev


class Docker:
    def __init__(self):
        self.client = docker.from_env()

    def containers(self):
        return self.client.containers.list()

    def images(self):
        return self.client.images.list()

    def run_detached(self, image_name):
        return self.client.containers.run(image_name, detach=True)

class Docker_Jupyter(Docker):

    def __init__(self,image_name):
        self.docker      = Docker()
        self.image_name  = image_name
        self._server     = 'http://localhost:8888'
        self._container  = None

    def container(self):
        if self._container is None:
            for container in self.docker.containers():
                if container.image.tags[0] == self.image_name:
                    self._container = container
        return self._container


    def logs(self):
        if self.running():
            return self.container().logs().decode()

    def start(self):
        return self.docker.run_detached(image_name=self.image_name)

    def stop(self):
        if self.container():
            self.container().stop()
            return True
        return False

    def running(self):
        return self.container() is not None

    def token(self):
        def find_in(array, text):
            return [item for item in reversed(array) if text in item]
        try:
            messages = self.logs().split('\n')
            jupyter_token  = find_in(messages, 'token=')[0].split('token=')[1].strip()
            return jupyter_token
        except:
            return None

    def server(self):
        return self._server
    
    def url(self):
        return "{0}?token={1}".format(self.server(),self.token())

