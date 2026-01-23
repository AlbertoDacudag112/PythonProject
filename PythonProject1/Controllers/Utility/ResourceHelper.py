import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ResourceHelper:
    """Helper class for loading resources like images consistently"""

    _project_root = None

    @classmethod
    def get_project_root(cls):
        if cls._project_root is None:
            current_file = os.path.abspath(__file__)
            utility_dir = os.path.dirname(current_file)
            cls._project_root = os.path.dirname(utility_dir)
        return cls._project_root

    @classmethod
    def get_resource_path(cls, filename, subfolder="Icons"):
        project_root = cls.get_project_root()
        resource_path = os.path.join(project_root, subfolder, filename)

        if os.path.exists(resource_path):
            return resource_path

        # Fallback locations
        alternatives = [
            os.path.join(project_root, "icons", filename),
            os.path.join(project_root, "Images", filename),
            os.path.join(project_root, "images", filename),
            os.path.join(project_root, "Assets", filename),
            os.path.join(project_root, "assets", filename),
        ]

        for alt in alternatives:
            if os.path.exists(alt):
                return alt

        print(f"[ResourceHelper] Resource not found: {filename}")
        return None

    @classmethod
    def load_pixmap(cls, filename, width=None, height=None, subfolder="Icons"):
        path = cls.get_resource_path(filename, subfolder)

        if not path:
            return None

        pixmap = QPixmap(path)
        if pixmap.isNull():
            return None

        if width and height:
            pixmap = pixmap.scaled(
                width,
                height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

        return pixmap
