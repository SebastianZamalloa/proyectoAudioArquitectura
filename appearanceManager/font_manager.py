class FontManager(object):
    """ font sizes need to be different on operating systems
        because on windows the text is displayed much larger """
    def __init__(self):
        self.button_font = ("Century Gothic", 14)
        self.note_display_font = ("Century Gothic", 50)
        self.note_display_font_medium = ("Century Gothic", 16)
        self.frequency_text_font = ("Century Gothic", 13)
        self.chord_text_font = ("Century Gothic", 25)
        self.info_text_font = ("Century Gothic", 12)
        self.settings_text_font = ("Century Gothic", 20)
