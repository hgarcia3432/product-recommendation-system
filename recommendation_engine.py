import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

class ProductRecommender:
    def __init__(self):
        self.products_df = None
        self.purchases_df = None
        
    def load_data(self, products_file, purchases_file):
        try:
            # Leer los archivos CSV
            self.products_df = pd.read_csv(products_file)
            self.purchases_df = pd.read_csv(purchases_file)
            
            # Limpiar nombres de columnas (eliminar espacios)
            self.products_df.columns = self.products_df.columns.str.strip()
            self.purchases_df.columns = self.purchases_df.columns.str.strip()
            
            print("✅ Datos cargados exitosamente!")
            print(f"📊 Productos cargados: {len(self.products_df)}")
            print(f"🛒 Compras cargadas: {len(self.purchases_df)}")
            
            # Verificar columnas
            print(f"📋 Columnas en productos: {list(self.products_df.columns)}")
            print(f"📋 Columnas en compras: {list(self.purchases_df.columns)}")
            
            return True
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return False
    
    def create_recommendation_matrix(self):
        try:
            print("\n🔄 Creando matriz de recomendaciones...")
            
            # Crear matriz usuario-producto
            user_product_matrix = self.purchases_df.pivot_table(
                index='user_id', 
                columns='product_id', 
                aggfunc='size', 
                fill_value=0
            )
            print("✅ Matriz usuario-producto creada")
            
            # Calcular similitud entre productos
            print("🔢 Calculando similitudes...")
            product_similarity = cosine_similarity(user_product_matrix.T)
            similarity_df = pd.DataFrame(
                product_similarity,
                index=user_product_matrix.columns,
                columns=user_product_matrix.columns
            )
            print("✅ Matriz de similitud calculada")
            
            return similarity_df
            
        except Exception as e:
            print(f"❌ Error creando matriz: {e}")
            return None
    
    def get_product_info(self, product_id):
        """Obtener información de un producto específico"""
        try:
            product_row = self.products_df[self.products_df['product_id'] == product_id]
            if len(product_row) == 0:
                return None
            return product_row.iloc[0]
        except:
            return None
    
    def get_recommendations(self, product_id, n_recommendations=3):
        try:
            similarity_df = self.create_recommendation_matrix()
            if similarity_df is None:
                return []
            
            # Obtener productos similares
            similar_products = similarity_df[product_id].sort_values(ascending=False)
            
            # Excluir el producto mismo y obtener recomendaciones
            recommendations = similar_products.drop(product_id).head(n_recommendations)
            
            # Obtener información de los productos recomendados
            recommended_products = []
            for rec_id, similarity in recommendations.items():
                product_info = self.get_product_info(rec_id)
                if product_info is not None:
                    recommended_products.append({
                        'product_id': rec_id,
                        'product_name': product_info['product_name'],
                        'category': product_info['category'],
                        'price': product_info['price'],
                        'similarity_score': round(similarity, 3)
                    })
            
            return recommended_products
            
        except Exception as e:
            print(f"❌ Error obteniendo recomendaciones para producto {product_id}: {e}")
            return []

def main():
    print("🚀 SISTEMA DE RECOMENDACIÓN - DEMO")
    print("=" * 50)
    
    # Crear recomendador
    recommender = ProductRecommender()
    
    # Cargar datos
    if not recommender.load_data('data/sample_products.csv', 'data/sample_purchases.csv'):
        print("❌ No se pudieron cargar los datos. Saliendo...")
        return
    
    print("\n" + "=" * 50)
    print("🎯 PROBANDO RECOMENDACIONES")
    print("=" * 50)
    
    # Probar con algunos productos
    test_products = [1, 3]  # iPhone 13 y AirPods Pro
    
    for product_id in test_products:
        print(f"\n" + "─" * 40)
        
        # Obtener información del producto
        product_info = recommender.get_product_info(product_id)
        if product_info is None:
            print(f"❌ Producto ID {product_id} no encontrado")
            continue
            
        print(f"🔍 Clientes que compraron: {product_info['product_name']} (${product_info['price']})")
        print(f"   Categoría: {product_info['category']}")
        
        # Obtener recomendaciones
        recommendations = recommender.get_recommendations(product_id, 3)
        
        if recommendations:
            print("   También compraron:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}️⃣ {rec['product_name']} - ${rec['price']} (Similitud: {rec['similarity_score']})")
        else:
            print("   ❌ No se encontraron recomendaciones")

    print("\n" + "=" * 50)
    print("✅ DEMO COMPLETADA")
    print("=" * 50)

if __name__ == "__main__":
    main()