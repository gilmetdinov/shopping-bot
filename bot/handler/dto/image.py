class ImageDto:

    def __init__(self, url=None, path=None, name=None):
        self.url = url
        self.path = path
        self.name = name

    def set_image_url(self, url):
        self.url = url

    def set_image_path(self, path):
        self.path = path

    def set_image_name(self, name):
        self.name = name

    def set_image(self, url, path, name):
        self.url = url
        self.path = path
        self.name = name

    def validate(self):
        if not self.url or not self.path or not self.name:
            return False
        return True

    def get_data(self):
        return {
            'url': self.url,
            'path': self.path,
            'name': self.name
        }
