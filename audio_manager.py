class audio_manger:
    def __init__(self):
        self.audio_file_path = 'None'
        self.audio = None
        self.audio_thread = None
        self.audio_player = None
        self.audio_player_thread = None
        self.audio_player_lock = threading.Lock()
