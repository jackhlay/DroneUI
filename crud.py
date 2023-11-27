import tkinter as tk

class CRUD:
    def __init__(self, root) -> tk:
        self.root = root
        self.root.title("bruh test")

        self.list = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.list.pack(pady=10)

        self.entru = tk.Entry(root)
        self.entru.pack(pady = 3)

        self.addButton = tk.Button(root, text="Add", command=lambda: self.add(self.entru.get())).pack(pady=5)
        self.removeButton = tk.Button(root, text="Remove", command=self.remove()).pack(pady=5)


    def getRoot(self):
        return self.root


    def add(self, item):
        self.list.insert(tk.END, item)

    def remove(self):
        selected= self.list.curselection()
        if selected:
            self.list.delete(selected)

if __name__ == "__main__":
    root = tk.Tk()
    c = CRUD(root)
    root.mainloop()
