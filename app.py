import customtkinter as ctk
from styling import *

class WindowState:
    def __init__(self):
        self.current_view = ""
        self.isOpen = False
        self.buton

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern Arayüz")
        self.geometry("900x600")

        ctk.set_appearance_mode("dark")
        self.configure(fg_color=BACKGROUND_COLOR)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=140, corner_radius=0, fg_color=SIDEBAR_COLOR)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="Menü", font=ctk.CTkFont(size=20, weight="bold"), text_color=TEXT_COLOR
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        button_params = {
            "fg_color": BUTTON_COLOR,
            "hover_color": BUTTON_HOVER_COLOR,
            "text_color": TEXT_COLOR,
        }
     
        self.home_button = ctk.CTkButton(
            self.sidebar, text="Ana Sayfa", command=lambda: self.switch_view(HomePage), **button_params
        )
        self.home_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.library_button = ctk.CTkButton(
            self.sidebar, text="Kütüphane", command=lambda: self.switch_view(LibraryPage), **button_params
        )
        self.library_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.lists_button = ctk.CTkButton(
            self.sidebar, text="Listeler", command=lambda: self.switch_view(ListsPage), **button_params
        )
        self.lists_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=CONTENT_BACKGROUND_COLOR)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.current_view = None
        self.after(10, self.switch_view, HomePage)  # Initial view after mainloop

    def switch_view(self, view_class):
        if self.current_view:
            self.current_view.destroy()

        self.current_view = view_class(self.content_frame)
        self.current_view.grid(row=0, column=0, sticky="nsew")


class BasePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=CONTENT_BACKGROUND_COLOR)
        self.app=app
        # Tüm alanı kaplamak için grid yapılandırması
        self.grid_rowconfigure(0, weight=1)  # Yatayda ortala
        self.grid_columnconfigure(0, weight=1)  # Dikeyde ortala
        
        FONT = ctk.CTkFont(size=20)
        self.label = ctk.CTkLabel(
            self, 
            text="", 
            font=FONT, 
            text_color=TEXT_COLOR,
            anchor="center"  # Metni label içinde ortala
        )
        
        # Label'ı hem yatay hem dikeyde ortala
        self.label.grid(row=0, column=0, sticky="nsew")

class HomePage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Grid yapılandırması (3 satırlık)
        self.grid_rowconfigure(0, weight=0)  # Araç çubuğu için
        self.grid_rowconfigure(1, weight=1)  # İçerik için
        self.grid_columnconfigure(0, weight=1)
        
        # Araç Çubuğu
        self.toolbar = ctk.CTkFrame(
            self, 
            fg_color=TOOLBAR_COLOR,  # styling.py'de tanımlı olmalı
            height=40
        )
        self.toolbar.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        
        # Araç çubuğu içeriği
        self.add_toolbar_components()
        
        # Ana içerik
        self.label.configure(
            text="Ana Sayfa İçeriği",
            font=ctk.CTkFont(size=30, weight="bold"))
        self.label.grid(row=1, column=0, sticky="nsew")

    def add_toolbar_components(self):
        # Buton stilleri
        btn_style = {
            "width": 100,
            "height": 30,
            "fg_color": BUTTON_COLOR,
            "hover_color": BUTTON_HOVER_COLOR,
            "text_color": TEXT_COLOR
        }
        
        # Dosya butonu
        self.btn_file = ctk.CTkButton(
            self.toolbar,
            text="Dosya",
            **btn_style
        )
        self.btn_file.pack(side="left", padx=5)
        
        # Düzenle butonu
        self.btn_edit = ctk.CTkButton(
            self.toolbar,
            text="Düzenle",
            **btn_style
        )
        self.btn_edit.pack(side="left", padx=5)
        
        # Ayırıcı
        ctk.CTkLabel(
            self.toolbar, 
            text="|", 
            text_color=SEPARATOR_COLOR
        ).pack(side="left", padx=5)
        
        # Arama çubuğu
        self.search_entry = ctk.CTkEntry(
            self.toolbar,
            width=200,
            placeholder_text="Arama...",
            fg_color=ENTRY_BG_COLOR
        )
        self.search_entry.pack(side="right", padx=5)

class LibraryPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.label.configure(text="Kütüphane İçeriği")


class ListsPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.label.configure(text="Listeler İçeriği")


if __name__ == "__main__":
    app = App()
    app.mainloop()
