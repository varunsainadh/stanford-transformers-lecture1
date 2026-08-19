import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import os
from chatbot import OSChatbot

class ChatbotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Prompt Deployer (Tkinter)")
        self.root.geometry("650x750")
        self.root.configure(bg="#f0f0f0")

        # Top Frame for System Prompt Selection
        top_frame = tk.Frame(self.root, bg="#e0e0e0", pady=10, padx=10)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Select System Prompt:", bg="#e0e0e0", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        
        self.prompt_var = tk.StringVar()
        self.prompt_dropdown = ttk.Combobox(top_frame, textvariable=self.prompt_var, state="readonly", font=("Arial", 11), width=30)
        self.prompt_dropdown.pack(side=tk.LEFT)
        
        # Load available prompts
        self.load_prompts()
        self.prompt_dropdown.bind("<<ComboboxSelected>>", self.on_prompt_change)

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, font=("Arial", 12),
            bg="#ffffff", state=tk.DISABLED
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        # Input entry
        self.input_entry = tk.Entry(input_frame, font=("Arial", 14))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(
            input_frame, text="Send", font=("Arial", 12, "bold"),
            bg="#4CAF50", fg="white", command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)

        # Initialize chatbot base
        self.chatbot = OSChatbot()
        self.append_message("System", "Select a prompt from the dropdown above to initialize the AI.")

    def load_prompts(self):
        prompts_dir = "SYSTEM_PROMPTS"
        if os.path.exists(prompts_dir):
            files = [f for f in os.listdir(prompts_dir) if f.endswith(".txt")]
            self.prompt_dropdown['values'] = files
        else:
            self.prompt_dropdown['values'] = []

    def on_prompt_change(self, event=None):
        selected = self.prompt_var.get()
        if selected:
            self.append_message("System", f"Switching persona to '{selected}'...")
            threading.Thread(target=self.init_chatbot, args=(selected,), daemon=True).start()

    def init_chatbot(self, prompt_filename):
        try:
            # Disable inputs while initializing
            self.send_button.config(state=tk.DISABLED)
            self.input_entry.config(state=tk.DISABLED)

            self.chatbot.initialize_with_prompt(prompt_filename)
            self.append_message("System", f"Chatbot is ready with prompt: {prompt_filename}")
            
            # Re-enable inputs
            self.send_button.config(state=tk.NORMAL)
            self.input_entry.config(state=tk.NORMAL)
        except Exception as e:
            self.append_message("System", f"Failed to initialize chatbot: {str(e)}")

    def append_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: ", "bold")
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Configure tag for bold text
        self.chat_display.tag_config("bold", font=("Arial", 12, "bold"))
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def send_message(self, event=None):
        if not self.chatbot.chat:
            self.append_message("System", "Please select a System Prompt first.")
            return

        user_text = self.input_entry.get().strip()
        if not user_text:
            return

        if user_text.lower() in ['exit', 'bye', 'quit']:
            self.root.quit()
            return

        self.input_entry.delete(0, tk.END)
        self.append_message("You", user_text)

        # Run bot response in a separate thread to avoid freezing UI
        threading.Thread(target=self.get_bot_response, args=(user_text,), daemon=True).start()

    def get_bot_response(self, text):
        # Disable button/entry while processing
        self.send_button.config(state=tk.DISABLED)
        self.input_entry.config(state=tk.DISABLED)
        
        response = self.chatbot.send_message(text)
        self.append_message("Chatbot", response)
        
        # Re-enable
        self.send_button.config(state=tk.NORMAL)
        self.input_entry.config(state=tk.NORMAL)
        self.input_entry.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotUI(root)
    root.mainloop()
