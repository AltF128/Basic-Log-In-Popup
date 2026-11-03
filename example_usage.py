import customtkinter as ctk
import page

class ExampleUsage(ctk.CTk):
    # Initialize the ExampleUsage class
    def __init__(self):
        super().__init__()

        # Set green to accent color
        ctk.set_default_color_theme("green")

        # Define the window title and size
        self.title("Example Usage")
        self.geometry("400x300")

        # Create a button to open the login popup
        self.open_login_popup_button = ctk.CTkButton(self, text="Open Log In Popup", command=self.open_login_popup)
        self.open_login_popup_button.pack(pady=20)

    def open_login_popup(self):
        page.load_login_popup(self)

if __name__ == "__main__":
    app = ExampleUsage()
    app.mainloop()
    