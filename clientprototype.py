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
            chat_log_text.insert('end', f'Another person: {message}\n')
            chat_log_text.configure(state='disabled')
        except:
            
            print('Disconnected from server')
            client.close()
            break

def send_message(message_entry, chat_log_text):
    message = message_entry.get()
    message_entry.delete(0, 'end')
    chat_log_text.configure(state='normal')
    chat_log_text.insert('end', f'You: {message}\n')
    chat_log_text.configure(state='disabled')
    client.send(message.encode('utf-8'))

def connect(ip_address, port_number):
    client.connect((ip_address, port_number))
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

message_entry = tk.Entry(root)
message_entry.pack(fill='x')

send_button = tk.Button(root, text='Send', command=lambda: send_message(message_entry, chat_log_text))
send_button.pack(fill='x')

connect('127.0.0.1', 55555)

root.protocol('WM_DELETE_WINDOW', on_closing)

root.mainloop()
