BLACK = 0
RED = 1
GREEN = 2
YELLOW = 3
BLUE = 4
MAGENTA = 5
CYAN = 6
WHITE = 7

BRIGHT = 8

RESET = '\x1b[0m'

def color_seq(color):
    if color & BRIGHT:
        return f'\x1b[{(color & 7) + 30};1m'
    else:
        return f'\x1b[{(color & 7) + 30}m'

def colorify(text, color):
    return color_seq(color) + text + RESET


class Colorizer:
    @staticmethod
    def mod_key(mod_key):
        return colorify(mod_key, WHITE+BRIGHT)
    
    @staticmethod
    def mod_name(mod_name):
        return colorify(mod_name, YELLOW+BRIGHT)
    
    @staticmethod
    def mod_owner(mod_owner):
        return colorify(mod_owner, GREEN+BRIGHT)
    
    @staticmethod
    def mod_blurb(mod_blurb):
        return colorify(mod_blurb, WHITE)
    
    @staticmethod
    def mod_category(mod_category):
        return colorify(mod_category, BLUE+BRIGHT)
    
    @staticmethod
    def file_name(file_name):
        return colorify(file_name, CYAN)
    
    @staticmethod
    def file_hash(file_hash):
        return colorify(file_hash, MAGENTA)
    
    @staticmethod
    def url(url):
        return colorify(url, BLUE)
    
    @staticmethod
    def emph(text):
        return colorify(text, BRIGHT)
    
    @staticmethod
    def ok(text):
        return colorify(text, GREEN+BRIGHT)
    
    @staticmethod
    def warn(text):
        return colorify(text, YELLOW+BRIGHT)
    
    @staticmethod
    def error(text):
        return colorify(text, RED+BRIGHT)
    
    @staticmethod
    def cli(cli):
        return colorify(cli, MAGENTA+BRIGHT)