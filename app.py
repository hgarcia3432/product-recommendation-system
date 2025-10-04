from flask import Flask, render_template, request, jsonify, send_from_directory
import recommendation_engine as re
import pandas as pd
import os

app = Flask(__name__)

# Servir archivos estáticos desde la carpeta data
@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory('data', filename)

@app.route('/')
def home():
    """Página principal del proyecto"""
    return render_template('index.html')

@app.route('/recommend/<int:product_id>')
def get_recommendations(product_id):
    """Endpoint para obtener recomendaciones"""
    try:
        print(f"🎯 Solicitando recomendaciones para producto: {product_id}")
        
        # Crear una nueva instancia del recomendador
        recommender = re.ProductRecommender()
        
        # Cargar datos
        if not recommender.load_data('data/sample_products.csv', 'data/sample_purchases.csv'):
            return jsonify({'success': False, 'error': 'No se pudieron cargar los datos'})
        
        # Obtener información del producto
        product_info = recommender.get_product_info(product_id)
        if product_info is None:
            return jsonify({'success': False, 'error': f'Producto {product_id} no encontrado'})
        
        # Obtener recomendaciones
        recommendations = recommender.get_recommendations(product_id, 3)
        
        print(f"✅ Recomendaciones encontradas: {len(recommendations)}")
        
        return jsonify({
            'success': True,
            'product': {
                'product_id': product_id,
                'product_name': product_info['product_name'],
                'category': product_info['category'],
                'price': product_info['price']
            },
            'recommendations': recommendations
        })
        
    except Exception as e:
        print(f"❌ Error en recomendaciones: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Ruta para ver todos los productos en JSON (para debugging)
@app.route('/api/products')
def api_products():
    try:
        products_df = pd.read_csv('data/sample_products.csv')
        return jsonify(products_df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🚀 Servidor de recomendación iniciado!")
    print("📱 Accede en: http://localhost:5000")
    print("🔧 Debug: http://localhost:5000/api/products")
    print("⚠️  Presiona CTRL+C para detener el servidor")
    app.run(debug=True, host='0.0.0.0', port=5000)