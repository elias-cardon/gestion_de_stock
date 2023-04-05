import tkinter as tk
from tkinter import ttk, messagebox
from db import Database

class ProductForm:
    def __init__(self, master, db, refresh_callback, product_id=None):
        self.master = master
        self.db = db
        self.refresh_callback = refresh_callback
        self.product_id = product_id

        self.form_window = tk.Toplevel(self.master)
        self.form_window.title("Formulaire Produit")

        ttk.Label(self.form_window, text="Nom").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        ttk.Label(self.form_window, text="Description").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        ttk.Label(self.form_window, text="Prix").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        ttk.Label(self.form_window, text="Quantité").grid(row=3, column=0, padx=10, pady=10, sticky='w')
        ttk.Label(self.form_window, text="ID Catégorie").grid(row=4, column=0, padx=10, pady=10, sticky='w')

        self.name_entry = ttk.Entry(self.form_window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.description_entry = ttk.Entry(self.form_window)
        self.description_entry.grid(row=1, column=1, padx=10, pady=10)
        self.price_entry = ttk.Entry(self.form_window)
        self.price_entry.grid(row=2, column=1, padx=10, pady=10)
        self.quantity_entry = ttk.Entry(self.form_window)
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=10)
        self.category_id_entry = ttk.Entry(self.form_window)
        self.category_id_entry.grid(row=4, column=1, padx=10, pady=10)

        if product_id is not None:
            self.load_product_data()

        submit_button = ttk.Button(self.form_window, text="Soumettre", command=self.submit_form)
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def load_product_data(self):
        product_data = self.db.fetch_product_by_id(self.product_id)
        if product_data is not None:
            self.name_entry.insert(0, product_data['nom'])
            self.description_entry.insert(0, product_data['description'])
            self.price_entry.insert(0, product_data['prix'])
            self.quantity_entry.insert(0, product_data['quantite'])
            self.category_id_entry.insert(0, product_data['id_categorie'])

    def submit_form(self):
        product = {
            'nom': self.name_entry.get(),
            'description': self.description_entry.get(),
            'prix': int(self.price_entry.get()),
            'quantite': int(self.quantity_entry.get()),
            'id_categorie': int(self.category_id_entry.get())
        }

        if self.product_id is None:
            self.db.add_product(product)
            messagebox.showinfo("Succès", "Produit ajouté avec succès")
        else:
            product['id'] = self.product_id
            self.db.update_product(product)
            messagebox.showinfo("Succès", "Produit modifié avec succès")

        self.refresh_callback()
        self.form_window.destroy()
