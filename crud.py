import tkinter as tk

class CRUD:
    def __init__(self, root) -> tk:
        self.root = root
        self.root.title("bruh test")

        self.vList = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.vList.pack(pady=10)

        self.entru = tk.Entry(root)
        self.entru.pack(pady = 3)

        self.addButton = tk.Button(root, text="Add", command=lambda: self.add(self.entru.get())).pack(pady=5)
        self.removeButton = tk.Button(root, text="Remove", command=self.remove).pack(pady=5)


    def getRoot(self):
        return self.root


    def add(self, item):
        self.vList.insert(tk.END, item)
        self.entru.delete(0, tk.END)  # clears entry box after adding item to vListbox

    def remove(self):
        print("selected: ", self.vList.curselection()[0])
        self.vList.delete(self.vList.curselection()[0])

if __name__ == "__main__":
    root = tk.Tk()
    c = CRUD(root)
    root.mainloop()