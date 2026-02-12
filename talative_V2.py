import customtkinter as ctk
from tkinter import messagebox
import json
from datetime import datetime
import os

class TalkativeApp:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.load_data()
        
        # Setup custom color theme
        ctk.set_appearance_mode("dark")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Talkative")
        self.root.geometry("1000x650")
        self.root.configure(fg_color="#0a0a0a")
        
        self.show_login_screen()
        
    def load_data(self):
        if os.path.exists('talkative_data.json'):
            with open('talkative_data.json', 'r') as f:
                data = json.load(f)
                self.users = data.get('users', {})
    
    def save_data(self):
        with open('talkative_data.json', 'w') as f:
            json.dump({'users': self.users}, f, indent=2)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        self.clear_window()
        
        main_frame = ctk.CTkFrame(self.root, fg_color="#0a0a0a")
        main_frame.pack(expand=True)
        
        # Title
        title_frame = ctk.CTkFrame(main_frame, fg_color="#1a0a2e", corner_radius=15)
        title_frame.pack(pady=30, padx=40, fill="x")
        
        ctk.CTkLabel(title_frame, text="💬 Talkative", 
                    font=("Arial", 36, "bold"),
                    text_color="#bb86fc").pack(pady=20)
        
        ctk.CTkLabel(title_frame, text="Connect. Chat. Communicate.", 
                    font=("Arial", 14),
                    text_color="#808080").pack(pady=(0, 20))
        
        # Login form
        form_frame = ctk.CTkFrame(main_frame, fg_color="#1a0a2e", corner_radius=15)
        form_frame.pack(pady=20, padx=40, fill="x")
        
        ctk.CTkLabel(form_frame, text="Username", 
                    font=("Arial", 12),
                    text_color="#bb86fc").pack(pady=(20, 5), anchor="w", padx=30)
        username_entry = ctk.CTkEntry(form_frame, width=300, height=40,
                                     fg_color="#2d1b4e",
                                     border_color="#bb86fc",
                                     text_color="white")
        username_entry.pack(pady=5, padx=30)
        
        ctk.CTkLabel(form_frame, text="Password", 
                    font=("Arial", 12),
                    text_color="#bb86fc").pack(pady=(15, 5), anchor="w", padx=30)
        password_entry = ctk.CTkEntry(form_frame, width=300, height=40, show="●",
                                     fg_color="#2d1b4e",
                                     border_color="#bb86fc",
                                     text_color="white")
        password_entry.pack(pady=5, padx=30)
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            if username in self.users:
                if self.users[username]['password'] == password:
                    self.current_user = username
                    self.show_main_screen()
                else:
                    messagebox.showerror("Error", "Incorrect password")
            else:
                messagebox.showerror("Error", "User not found")
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            if username in self.users:
                messagebox.showerror("Error", "Username already exists")
                return
            
            self.users[username] = {
                'password': password,
                'messages': [],
                'status': 'Hey there! I am using Talkative'
            }
            self.save_data()
            messagebox.showinfo("Success", "Account created! You can now login.")
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="Login", command=login,
                     width=140, height=40,
                     fg_color="#6200ea",
                     hover_color="#7c4dff",
                     corner_radius=20,
                     font=("Arial", 14, "bold")).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="Register", command=register,
                     width=140, height=40,
                     fg_color="#2d1b4e",
                     hover_color="#3d2b5e",
                     border_width=2,
                     border_color="#bb86fc",
                     corner_radius=20,
                     font=("Arial", 14, "bold")).pack(side="left", padx=5)
        
        password_entry.bind("<Return>", lambda e: login())
    
    def show_main_screen(self):
        self.clear_window()
        
        # Sidebar
        sidebar = ctk.CTkFrame(self.root, width=280, fg_color="#1a0a2e", corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # User profile section
        profile_frame = ctk.CTkFrame(sidebar, fg_color="#2d1b4e", corner_radius=10)
        profile_frame.pack(pady=20, padx=15, fill="x")
        
        ctk.CTkLabel(profile_frame, text="👤", font=("Arial", 32)).pack(pady=(15, 5))
        ctk.CTkLabel(profile_frame, text=self.current_user, 
                    font=("Arial", 16, "bold"),
                    text_color="#bb86fc").pack()
        ctk.CTkLabel(profile_frame, text=self.users[self.current_user]['status'], 
                    font=("Arial", 10),
                    text_color="#808080",
                    wraplength=220).pack(pady=(5, 15), padx=10)
        
        # Search bar
        search_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        search_frame.pack(pady=10, padx=15, fill="x")
        
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search users...",
                                   fg_color="#2d1b4e",
                                   border_color="#bb86fc",
                                   height=35)
        search_entry.pack(fill="x")
        
        # Users list
        ctk.CTkLabel(sidebar, text="Users", 
                    font=("Arial", 14, "bold"),
                    text_color="#bb86fc").pack(pady=(10, 5), anchor="w", padx=15)
        
        users_scroll = ctk.CTkScrollableFrame(sidebar, fg_color="transparent")
        users_scroll.pack(fill="both", expand=True, padx=15, pady=10)
        
        def update_user_list():
            for widget in users_scroll.winfo_children():
                widget.destroy()
            
            search_term = search_entry.get().lower()
            
            for username in self.users:
                if username == self.current_user:
                    continue
                
                if search_term and search_term not in username.lower():
                    continue
                
                # Get unread count
                unread = sum(1 for msg in self.users[self.current_user]['messages'] 
                           if msg['from'] == username and not msg.get('read', False))
                
                user_btn = ctk.CTkButton(
                    users_scroll,
                    text=f"{username}" + (f"  ({unread})" if unread > 0 else ""),
                    command=lambda u=username: self.open_chat(u),
                    fg_color="#2d1b4e" if unread == 0 else "#6200ea",
                    hover_color="#3d2b5e",
                    height=50,
                    anchor="w",
                    font=("Arial", 13)
                )
                user_btn.pack(fill="x", pady=3)
        
        update_user_list()
        search_entry.bind("<KeyRelease>", lambda e: update_user_list())
        
        # Logout button
        ctk.CTkButton(sidebar, text="Logout", command=self.show_login_screen,
                     fg_color="#1a0a2e",
                     hover_color="#0a0a0a",
                     border_width=2,
                     border_color="#bb86fc",
                     height=40).pack(side="bottom", pady=15, padx=15, fill="x")
        
        # Chat area
        self.chat_container = ctk.CTkFrame(self.root, fg_color="#0a0a0a")
        self.chat_container.pack(side="right", fill="both", expand=True)
        
        # Welcome message
        welcome_frame = ctk.CTkFrame(self.chat_container, fg_color="transparent")
        welcome_frame.pack(expand=True)
        
        ctk.CTkLabel(welcome_frame, text="💬", font=("Arial", 64)).pack()
        ctk.CTkLabel(welcome_frame, text="Select a user to start chatting", 
                    font=("Arial", 18),
                    text_color="#808080").pack(pady=10)
    
    def open_chat(self, other_user):
        for widget in self.chat_container.winfo_children():
            widget.destroy()
        
        # Mark messages as read
        for msg in self.users[self.current_user]['messages']:
            if msg['from'] == other_user:
                msg['read'] = True
        self.save_data()
        
        # Chat header
        header = ctk.CTkFrame(self.chat_container, height=70, fg_color="#1a0a2e", corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(expand=True, fill="both", padx=20)
        
        ctk.CTkLabel(header_content, text="👤", font=("Arial", 28)).pack(side="left", padx=(0, 15))
        
        user_info = ctk.CTkFrame(header_content, fg_color="transparent")
        user_info.pack(side="left", fill="y")
        
        ctk.CTkLabel(user_info, text=other_user, 
                    font=("Arial", 18, "bold"),
                    text_color="#bb86fc").pack(anchor="w")
        ctk.CTkLabel(user_info, text=self.users[other_user]['status'], 
                    font=("Arial", 10),
                    text_color="#808080").pack(anchor="w")
        
        # Messages area
        messages_frame = ctk.CTkScrollableFrame(self.chat_container, fg_color="#0a0a0a")
        messages_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        def display_messages():
            for widget in messages_frame.winfo_children():
                widget.destroy()
            
            # Collect all messages between both users
            all_msgs = []
            for msg in self.users[self.current_user]['messages']:
                if msg['from'] == other_user or msg['to'] == other_user:
                    all_msgs.append(msg)
            
            for msg in self.users[other_user]['messages']:
                if msg['from'] == self.current_user or msg['to'] == self.current_user:
                    if msg not in all_msgs:
                        all_msgs.append(msg)
            
            all_msgs.sort(key=lambda x: x['timestamp'])
            
            for msg in all_msgs:
                is_sent = msg['from'] == self.current_user
                
                msg_container = ctk.CTkFrame(messages_frame, fg_color="transparent")
                msg_container.pack(fill="x", pady=5)
                
                msg_bubble = ctk.CTkFrame(
                    msg_container,
                    fg_color="#6200ea" if is_sent else "#2d1b4e",
                    corner_radius=15
                )
                msg_bubble.pack(side="right" if is_sent else "left", padx=10)
                
                ctk.CTkLabel(msg_bubble, text=msg['text'], 
                           font=("Arial", 12),
                           text_color="white",
                           wraplength=400,
                           justify="left").pack(padx=15, pady=10, anchor="w")
                
                time_str = datetime.fromisoformat(msg['timestamp']).strftime("%I:%M %p")
                ctk.CTkLabel(msg_bubble, text=time_str, 
                           font=("Arial", 8),
                           text_color="#b0b0b0").pack(padx=15, pady=(0, 8), anchor="e")
        
        display_messages()
        
        # Input area
        input_frame = ctk.CTkFrame(self.chat_container, fg_color="#1a0a2e", height=80, corner_radius=0)
        input_frame.pack(fill="x", side="bottom")
        input_frame.pack_propagate(False)
        
        input_container = ctk.CTkFrame(input_frame, fg_color="transparent")
        input_container.pack(expand=True, fill="both", padx=20, pady=15)
        
        msg_entry = ctk.CTkEntry(input_container, 
                                placeholder_text="Type a message...",
                                height=50,
                                fg_color="#2d1b4e",
                                border_color="#bb86fc",
                                font=("Arial", 12))
        msg_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        def send_message():
            text = msg_entry.get().strip()
            if not text:
                return
            
            message = {
                'from': self.current_user,
                'to': other_user,
                'text': text,
                'timestamp': datetime.now().isoformat(),
                'read': False
            }
            
            self.users[self.current_user]['messages'].append(message)
            self.users[other_user]['messages'].append(message.copy())
            self.save_data()
            
            msg_entry.delete(0, 'end')
            display_messages()
            messages_frame._parent_canvas.yview_moveto(1.0)
        
        send_btn = ctk.CTkButton(input_container, text="Send",
                                command=send_message,
                                width=100, height=50,
                                fg_color="#6200ea",
                                hover_color="#7c4dff",
                                corner_radius=15,
                                font=("Arial", 14, "bold"))
        send_btn.pack(side="right")
        
        msg_entry.bind("<Return>", lambda e: send_message())
        msg_entry.focus()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TalkativeApp()
    app.run()