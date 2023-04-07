import pymysql

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Jobbax_La_Menace',
            database='boutique'
        )

    # Méthode pour exécuter les requêtes
    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        return cursor

    # Méthode pour récupérer tous les produits
    def fetch_all_products(self):
        query = "SELECT * FROM produit"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    # Méthode pour récupérer un produit par son ID
    def fetch_product_by_id(self, product_id):
        query = f"SELECT * FROM produit WHERE id={product_id}"
        cursor = self.execute_query(query)
        result = cursor.fetchone()

        if result:
            product = {
                'id': result[0],
                'nom': result[1],
                'description': result[2],
                'prix': result[3],
                'quantite': result[4],
                'id_categorie': result[5]
            }
            return product

        return None

    # Méthode pour ajouter un produit
    def add_product(self, product):
        query = f"INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES ('{product['nom']}', '{product['description']}', {product['prix']}, {product['quantite']}, {product['id_categorie']})"
        self.execute_query(query)

    # Méthode pour mettre à jour un produit
    def update_product(self, product):
        query = f"UPDATE produit SET nom='{product['nom']}', description='{product['description']}', prix={product['prix']}, quantite={product['quantite']}, id_categorie={product['id_categorie']} WHERE id={product['id']}"
        self.execute_query(query)

    # Méthode pour supprimer un produit
    def delete_product(self, product_id):
        query = f"DELETE FROM produit WHERE id={product_id}"
        self.execute_query(query)

    # Méthode pour fermer la connexion
    def close_connection(self):
        self.connection.close()