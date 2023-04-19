import tkinter as tk
import socket
import threading

root = tk.Tk()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive_messages(chat_log_text):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            chat_log_text.configure(state='normal')
            chat_log_text.insert('end', f'{message}\n')
            chat_log_text.configure(state='disabled')
        except:
            print('Disconnected from server')
            client.close()
            break

def send_message(username_entry, message_entry):
    username = username_entry.get()
    message = message_entry.get()
    message_entry.delete(0, 'end')
    chat_log_text.configure(state='normal')
    chat_log_text.insert('end', f'{username}: {message}\n')
    chat_log_text.configure(state='disabled')
    client.send(f'{username}: {message}'.encode('utf-8'))

def connect(ip_address, port_number, username_entry):
    username = username_entry.get()
    client.connect((ip_address, port_number))
    client.send(username.encode('utf-8'))
    receive_thread = threading.Thread(target=receive_messages, args=(chat_log_text,))
    receive_thread.start()

def on_closing():
    client.close()
    root.destroy()

# GUI
root.title('Chat App')
root.geometry('500x500')

chat_log_text = tk.Text(root, state='disabled')
chat_log_text.pack(fill='both', expand=True)

username_label = tk.Label(root, text='Username:')
username_label.pack()

username_entry = tk.Entry(root)
username_entry.pack(fill='x')

message_entry = tk.Entry(root)
message_entry.pack(fill='x')

send_button = tk.Button(root, text='Send', command=lambda: send_message(username_entry, message_entry))
send_button.pack(fill='x')

connect_button = tk.Button(root, text='Connect', command=lambda: connect('127.0.0.1', 55555, username_entry))
connect_button.pack(fill='x')

root.protocol('WM_DELETE_WINDOW', on_closing)

root.mainloop()
