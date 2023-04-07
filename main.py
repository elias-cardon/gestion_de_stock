# Importation des bibliothèques et modules nécessaires
import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial

from db import Database
from product_form import ProductForm

# Messages localisés
LOCALIZED_STRINGS = {
    "app_title": "Gestion des stocks",
    "error": "Erreur",
    "select_product_modify": "Veuillez sélectionner un produit à modifier",
    "select_product_delete": "Veuillez sélectionner un produit à supprimer"
}

class StockApp:
    def __init__(self, master):
        self.master = master
        self.master.title(LOCALIZED_STRINGS["app_title"])

        self.db = Database()

        self.create_widgets()
        self.load_products(limit=20, offset=0)

        # Centrer la fenêtre après la création des widgets
        self.center_window()

    # Méthode pour centrer la fenêtre sur l'écran
    def center_window(self):
        self.master.update_idletasks()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        x_position = int((screen_width / 2) - (window_width / 2)) - 95
        y_position = int((screen_height / 2) - (window_height / 2)) - 100
        self.master.geometry(f"+{x_position}+{y_position}")

    def create_widgets(self):
        # Création de l'arborescence pour afficher les produits
        self.tree = ttk.Treeview(
            self.master,
            columns=('id', 'nom', 'description', 'prix', 'quantite', 'id_categorie'),
            show='headings'
        )
        self.tree.column('id', width=50)
        self.tree.column('nom', width=150)
        self.tree.column('description', width=300)
        self.tree.column('prix', width=100)
        self.tree.column('quantite', width=100)
        self.tree.column('id_categorie', width=100)
        self.tree.heading('id', text='ID', command=partial(self.sort_column, "id"))
        self.tree.heading('nom', text='Nom', command=partial(self.sort_column, "nom"))
        self.tree.heading('description', text='Description', command=partial(self.sort_column, "description"))
        self.tree.heading('prix', text='Prix', command=partial(self.sort_column, "prix"))
        self.tree.heading('quantite', text='Quantité', command=partial(self.sort_column, "quantite"))
        self.tree.heading('id_categorie', text='ID Catégorie', command=partial(self.sort_column, "id_categorie"))
        self.tree.grid(row=0, column=0, columnspan=4, padx=20, pady=20, sticky='nsew')

        # Création des boutons pour les actions Ajouter, Modifier, Supprimer et Quitter
        add_button = ttk.Button(self.master, text='Ajouter', command=self.open_add_product_form)
        add_button.grid(row=1, column=0, pady=10)

        update_button = ttk.Button(self.master, text='Modifier', command=self.open_update_product_form)
        update_button.grid(row=1, column=1, pady=10)

        delete_button = ttk.Button(self.master, text='Supprimer', command=self.delete_product)
        delete_button.grid(row=1, column=2, pady=10)

        exit_button = ttk.Button(self.master, text='Quitter', command=self.master.quit)
        exit_button.grid(row=1, column=3, pady=10)

        # Ajout d'un champ de recherche
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self.master, textvariable=self.search_var)
        search_entry.grid(row=2, column=0, padx=20, pady=10)
        search_button = ttk.Button(self.master, text='Rechercher', command=self.search_product)
        search_button.grid(row=2, column=1, pady=10)

        # Ajout de la pagination
        self.current_page = 0
        previous_page_button = ttk.Button(self.master, text='Précédent', command=self.previous_page)
        previous_page_button.grid(row=2, column=2, pady=10)
        next_page_button = ttk.Button(self.master, text='Suivant', command=self.next_page)
        next_page_button.grid(row=2, column=3, pady=10)

        # Méthode pour rechercher un produit
    def search_product(self):
        search_query = self.search_var.get()
        if search_query:
            products = self.db.search_products(search_query)
            self.display_products(products)
        else:
            self.load_products()

    # Méthode pour passer à la page précédente
    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            offset = self.current_page * 20
            self.load_products(limit=20, offset=offset)

    # Méthode pour passer à la page suivante
    def next_page(self):
        self.current_page += 1
        offset = self.current_page * 20
        products = self.db.fetch_products(limit=20, offset=offset)
        if products:
            self.display_products(products)
        else:
            self.current_page -= 1

    # Méthode pour charger les produits depuis la base de données avec pagination
    def load_products(self, limit, offset):
        products = self.db.fetch_products(limit=limit, offset=offset)
        self.display_products(products)

    # Méthode pour afficher les produits dans l'arborescence
    def display_products(self, products):
        self.tree.delete(*self.tree.get_children())
        for product in products:
            self.tree.insert('', 'end', values=product)

    # Méthode pour trier les colonnes
    def sort_column(self, column):
        # Implémenter la logique de tri en fonction de la colonne sélectionnée
        pass

    # Méthode pour charger les produits depuis la base de données
    def load_products(self):
        products = self.db.fetch_all_products()
        self.tree.delete(*self.tree.get_children())
        for product in products:
            self.tree.insert('', 'end', values=product)

    # Méthode pour ouvrir le formulaire d'ajout de produit
    def open_add_product_form(self):
        product_form = ProductForm(self.master, self.db, self.load_products)

    # Méthode pour ouvrir le formulaire de modification de produit
    def open_update_product_form(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à modifier")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        product_form = ProductForm(self.master, self.db, self.load_products, product_id)

    # Méthode pour supprimer un produit
    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à supprimer")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        self.db.delete_product(product_id)
        self.load_products()

# Programme principal
if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()