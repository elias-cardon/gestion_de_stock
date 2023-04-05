import tkinter as tk
from tkinter import ttk, messagebox
from db import Database
from product_form import ProductForm

class StockApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestion des stocks")

        self.db = Database()

        self.create_widgets()

        self.load_products()

        # Centrer la fenêtre après la création des widgets
        self.center_window()

    def center_window(self):
        self.master.update_idletasks()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        x_position = int(
            (screen_width / 2) - (window_width / 2)) - 95  # Soustrayez 200 pour un décalage plus important à gauche
        y_position = int((screen_height / 2) - (window_height / 2)) - 100
        self.master.geometry(f"+{x_position}+{y_position}")

    def create_widgets(self):
        # Création des widgets
        self.tree = ttk.Treeview(self.master, columns=('id', 'nom', 'description', 'prix', 'quantite', 'id_categorie'), show='headings')
        self.tree.column('id', width=50)
        self.tree.column('nom', width=150)
        self.tree.column('description', width=300)
        self.tree.column('prix', width=100)
        self.tree.column('quantite', width=100)
        self.tree.column('id_categorie', width=100)
        self.tree.heading('id', text='ID')
        self.tree.heading('nom', text='Nom')
        self.tree.heading('description', text='Description')
        self.tree.heading('prix', text='Prix')
        self.tree.heading('quantite', text='Quantité')
        self.tree.heading('id_categorie', text='ID Catégorie')
        self.tree.grid(row=0, column=0, columnspan=4, padx=20, pady=20, sticky='nsew')

        add_button = ttk.Button(self.master, text='Ajouter', command=self.open_add_product_form)
        add_button.grid(row=1, column=0, pady=10)

        update_button = ttk.Button(self.master, text='Modifier', command=self.open_update_product_form)
        update_button.grid(row=1, column=1, pady=10)

        delete_button = ttk.Button(self.master, text='Supprimer', command=self.delete_product)
        delete_button.grid(row=1, column=2, pady=10)

        exit_button = ttk.Button(self.master, text='Quitter', command=self.master.quit)
        exit_button.grid(row=1, column=3, pady=10)

    def load_products(self):
        products = self.db.fetch_all_products()
        self.tree.delete(*self.tree.get_children())
        for product in products:
            self.tree.insert('', 'end', values=product)

    def open_add_product_form(self):
        product_form = ProductForm(self.master, self.db, self.load_products)

    def open_update_product_form(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à modifier")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        product_form = ProductForm(self.master, self.db, self.load_products, product_id)

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à supprimer")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        self.db.delete_product(product_id)
        self.load_products()

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
