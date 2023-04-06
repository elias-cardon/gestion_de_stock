import tkinter as tk
from tkinter import ttk, messagebox
from db import Database
from product_form import ProductForm


class StockApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestion des stocks")

        # Modifier la taille de la fenêtre
        window_width = 1000  # Ajuster la largeur de la fenêtre
        window_height = 500  # Ajuster la hauteur de la fenêtre
        self.master.geometry(f"{window_width}x{window_height}")

        self.db = Database()

        self.create_widgets()
        self.load_products()

    # Créer les widgets pour l'application
    def create_widgets(self):
        # Configuration de la table des produits
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

        # Création des boutons
        add_button = ttk.Button(self.master, text='Ajouter', command=self.open_add_product_form)
        add_button.grid(row=1, column=0, pady=10, padx=10)

        update_button = ttk.Button(self.master, text='Modifier', command=self.open_update_product_form)
        update_button.grid(row=1, column=1, pady=10, padx=10)

        delete_button = ttk.Button(self.master, text='Supprimer', command=self.delete_product)
        delete_button.grid(row=1, column=2, pady=10, padx=10)

        exit_button = ttk.Button(self.master, text='Quitter', command=self.master.quit)
        exit_button.grid(row=1, column=3, pady=10, padx=10)

        # Configuration de la mise en page
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

    # Charger les produits dans l'arborescence
    def load_products(self):
        products = self.db.fetch_all_products()
        self.tree.delete(*self.tree.get_children())
        for product in products:
            self.tree.insert('', 'end', values=product)

    # Ouvrir le formulaire pour ajouter un produit
    def open_add_product_form(self):
        product_form = ProductForm(self.master, self.db, self.load_products)

    # Ouvrir le formulaire pour modifier un produit
    def open_update_product_form(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à modifier")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        product_form = ProductForm(self.master, self.db, self.load_products, product_id)

    # Supprimer un produit
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