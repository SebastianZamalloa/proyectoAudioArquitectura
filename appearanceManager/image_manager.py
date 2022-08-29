
from PIL import Image
from PIL import ImageTk


class ImageManager(object):
    def __init__(self, main_path):
        self.bell_image = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/bell.png").resize((50, 50), Image.ANTIALIAS))

        self.bell_hovered_image = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/bell_hovered.png").resize((50, 50), Image.ANTIALIAS))

        self.bell_muted_image = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/mutedBell.png").resize((50, 50), Image.ANTIALIAS))

        self.bell_muted_hovered_image = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/mutedBell_hovered.png").resize((50, 50), Image.ANTIALIAS))

        self.arrowUp_image = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/arrowUp.png").resize((147, 46), Image.ANTIALIAS))

        self.arrowUp_image_hovered = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/arrowUp_hovered.png").resize((147, 46), Image.ANTIALIAS))

        self.arrowDown_image = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/arrowDown.png").resize((147, 46), Image.ANTIALIAS))

        self.arrowDown_image_hovered = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/arrowDown_hovered.png").resize((147, 46), Image.ANTIALIAS))
        
        self.do = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/do.png").resize((160, 100), Image.ANTIALIAS))
        
        self.do_plus = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/do_plus.png").resize((160, 100), Image.ANTIALIAS))

        self.re = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/re.png").resize((160, 100), Image.ANTIALIAS))
        
        self.re_plus = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/re_plus.png").resize((160, 100), Image.ANTIALIAS))
        
        self.mi = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/mi.png").resize((160, 100), Image.ANTIALIAS))
        
        self.fa = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/fa.png").resize((160, 100), Image.ANTIALIAS))
        
        self.fa_plus = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/fa_plus.png").resize((160, 100), Image.ANTIALIAS))
        
        self.sol = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/sol.png").resize((160, 100), Image.ANTIALIAS))
        
        self.sol_plus = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/sol_plus.png").resize((160, 100), Image.ANTIALIAS))
        
        self.la = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/la.png").resize((160, 100), Image.ANTIALIAS))
        
        self.la_plus = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/la_plus.png").resize((160, 100), Image.ANTIALIAS))

        self.si = ImageTk.PhotoImage(
            Image.open(main_path + "/assets/images/si.png").resize((160, 100), Image.ANTIALIAS))
