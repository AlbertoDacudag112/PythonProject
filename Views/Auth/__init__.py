def __init__(self):
    print("      → LoginView.__init__ started")
    super().__init__()
    print("      → QMainWindow initialized")

    self.setWindowTitle("RoadEye - Vehicle Violation Monitoring System")
    self.setFixedSize(450, 620)
    self.setStyleSheet("background-color: #2d2d2d;")
    print("      → Window properties set")

    print("      → Setting up UI...")
    self._setup_ui()
    print("      → LoginView UI setup complete")