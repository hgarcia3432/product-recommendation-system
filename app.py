from flask import Flask, render_template, request, jsonify
import recommendation_engine as re
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    """Página principal con lista de productos"""
    products = pd.read_csv('data/sample_products.csv').to_dict('records')
    return render_template('index.html', products=products)

@app.route('/recommend/<int:product_id>')
def get_recommendations(product_id):
    """Endpoint para obtener recomendaciones"""
    try:
        recommender = re.ProductRecommender()
        recommender.load_data('data/sample_products.csv', 'data/sample_purchases.csv')
        recommender.calculate_similarity()
        
        product_info = recommender.products_df[recommender.products_df['product_id'] == product_id].iloc[0].to_dict()
        recommendations = recommender.get_recommendations(product_id, 5)
        
        return jsonify({
            'success': True,
            'product': product_info,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("🚀 Servidor de recomendación iniciado!")
    print("📱 Accede en: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)