import customtkinter as ctk
import logic
import machineid

class LogInPopup(ctk.CTkToplevel):
    # Initialize the LogInPopup class
    def __init__(self, parent):
        super().__init__(parent)

        # Generate Key
        with open(f"{logic.get_parent_path()}/secret.key", "r") as f:
            if f.read() == "":
                logic.generate_key()

        # Window Size and Definition
        self.title("Log In Popup")
        self.geometry("300x400")
        self.resizable(False, False)

        logged_in_username = logic.check_machine_cookies()

        # Window Objects
        self.login_select = []
        self.logged_in = []
        self.login_page = []
        self.signup_page = []

        # Login Type Selection Page
        self.login_select.append(ctk.CTkLabel(self, text="Log In or Sign Up", font=ctk.CTkFont(size=20, weight="bold")))
        self.login_select.append(ctk.CTkButton(self, text="Log In", command=self.show_login_page))
        self.login_select.append(ctk.CTkButton(self, text="Sign Up", command=self.show_signup_page))

        # Already Logged in Page
        self.logged_in.append(ctk.CTkLabel(self, text=f"Already logged in as {logged_in_username}. Log out?"))
        self.logged_in.append(ctk.CTkButton(self, text="Log Out", command=self.log_out))

        # Login Page
        self.login_page.append(ctk.CTkLabel(self, text="Log In", font=ctk.CTkFont(size=20, weight="bold")))
        self.login_page.append(ctk.CTkEntry(self, placeholder_text="Username"))
        self.login_page.append(ctk.CTkEntry(self, placeholder_text="Password", show="*"))
        self.login_page.append(ctk.CTkButton(self, text="Log In", command=lambda: logic.handle_login(self.login_page[1].get(), self.login_page[2].get())))
        self.login_page.append(ctk.CTkButton(self, text="Back", command=self.show_select_page))
        self.login_page.append(ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12)))  # Placeholder for return message
        self.login_page[4].my_id = "changable_button"
        self.login_page[5].my_id = "status_message"

        # Signup Page
        self.signup_page.append(ctk.CTkLabel(self, text="Sign Up", font=ctk.CTkFont(size=20, weight="bold")))
        self.signup_page.append(ctk.CTkEntry(self, placeholder_text="Username"))
        self.signup_page.append(ctk.CTkEntry(self, placeholder_text="Password", show="*"))
        self.signup_page.append(ctk.CTkEntry(self, placeholder_text="Re-Enter Password", show="*"))
        self.signup_page.append(ctk.CTkButton(self, text="Sign Up", command=lambda: logic.handle_signup(self.signup_page[1].get(), self.signup_page[2].get(), self.signup_page[3].get())))
        self.signup_page.append(ctk.CTkButton(self, text="Back", command=self.show_select_page))
        self.signup_page.append(ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12)))  # Placeholder for return message
        self.signup_page[5].my_id = "changable_button"
        self.signup_page[6].my_id = "status_message"

        # Show the initial selection page
        if logged_in_username:
            for widget in self.logged_in:
                widget.pack(pady=10)
        else:
            for widget in self.login_select:
                widget.pack(pady=10)

        self.update_labels()

    def update_labels(self):
        for widget in self.login_page:
            if hasattr(widget, "my_id"):
                if widget.my_id == "status_message":
                    with open(f"{logic.get_parent_path()}/returns.txt", "r") as f:
                        file_data = f.read()
                        print(f"Changed Label text from: {widget.cget("text")} to {file_data}")
                        widget.configure(text=file_data)
                if widget.my_id == "changable_button":
                    if logic.check_machine_cookies():
                        widget.configure(text="Close")
                    else:
                        widget.configure(text="Back")

        for widget in self.signup_page:
            if hasattr(widget, "my_id"):
                if widget.my_id == "status_message":
                    with open(f"{logic.get_parent_path()}/returns.txt", "r") as f:
                        file_data = f.read()
                        print(f"Changed Label text from: {widget.cget("text")} to {file_data}")
                        widget.configure(text=file_data)
                if widget.my_id == "changable_button":
                    if logic.check_machine_cookies():
                        widget.configure(text="Close")
                    else:
                        widget.configure(text="Close")

        self.after("100", self.update_labels)

    def log_out(self):
        # Get machine id
        machine_id = machineid.id()

        # Save lines
        with open(f"{logic.get_parent_path()}/cookies.txt", "r") as cookies_file:
            lines = cookies_file.readlines()
            cookies_file.close()

        # Rewrite everything except the remove line
        with open(f"{logic.get_parent_path()}/cookies.txt", "w") as cookies_file:
            for line in lines:
                machine, username = line.strip().split(" $^&^$ ")
                if machine != machine_id:
                    cookies_file.write(line)

        # Go to the select page
        self.show_select_page()

    def show_login_page(self):
        # Hide the current page without destroying widgets that will be reused.
        for widget in self.winfo_children():
            logic.reset_status()  # Clear the contents of returns.txt when switching pages
            widget.pack_forget()

        # Create login page widgets
        for widget in self.login_page:
            widget.pack(pady=10)

    def show_signup_page(self):
        # Hide the current page without destroying widgets that will be reused.
        for widget in self.winfo_children():
            logic.reset_status()  # Clear the contents of returns.txt when switching pages
            widget.pack_forget()

        # Create signup page widgets
        for widget in self.signup_page:
            widget.pack(pady=10)

    def show_select_page(self):
        if logic.check_machine_cookies():
            self.destroy()

        else:
            # Hide the current page without destroying widgets that will be reused.
            for widget in self.winfo_children():
                logic.reset_status()  # Clear the contents of returns.txt when switching pages
                widget.pack_forget()

            # Create select page widgets
            for widget in self.login_select:
                widget.pack(pady=10)

    def show_logged_in_page(self):
        # Hide the current page without destroying widgets that will be reused.
        for widget in self.winfo_children():
            logic.reset_status()  # Clear the contents of returns.txt when switching pages
            widget.pack_forget()

        # Create select page widgets
        for widget in self.logged_in:
            widget.pack(pady=10)

def load_login_popup(parent):
    login_popup = LogInPopup(parent)
    login_popup.mainloop()

# Example usage:
# load_login_popup(your_parent_widget)