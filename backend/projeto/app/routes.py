from flask import Blueprint, request, jsonify
from flask_cors import CORS
import matplotlib
matplotlib.use("Agg")  # Modo sem interface gráfica

# Cria o blueprint principal
routes = Blueprint("routes", __name__)
CORS(routes)  # Habilita CORS para todas as rotas

# Importação das funções de geração
from app.generate_bst import generate_binary_tree
from app.generate_avl import generate_avl
from app.generate_fibonacci import generate_fibonacci_tree
from app.generate_btree import generate_b_tree
from app.hashes import generate_hashing_image
from app.listas import auto_list_operation, skip_list_operation

@routes.route("/generate_tree", methods=["POST"])
def generate_tree():
    try:
        data = request.json
        print("📥 Dados recebidos no backend:", data)

        tree_type = data.get("treeType")
        value = int(data.get("value", 10))

        if not tree_type or value <= 0:
            return jsonify({"error": "Parâmetros inválidos"}), 400

        if tree_type == "BST":
            search_num = data.get("searchNum")
            add_nodes = data.get("addNodes")
            image_base64 = generate_binary_tree(
                n_nodes=value,
                search_num=search_num,
                add_nodes=add_nodes
            )
        elif tree_type == "AVL":
            image_base64 = generate_avl(value)
        elif tree_type == "Fibonacci":
            image_base64 = generate_fibonacci_tree(value)
        elif tree_type == "BTree":
            add_num = data.get("addNum")
            search_num = data.get("searchNum")
            degree = int(data.get("degree", 2))
            image_base64 = generate_b_tree(
                n_nodes=value,
                add_num=add_num,
                search_num=search_num,
                t=degree
            )
        else:
            return jsonify({"error": "Tipo de árvore inválido"}), 400

        return jsonify({"image": image_base64})

    except Exception as e:
        print(f"❌ Erro no Flask: {str(e)}")
        return jsonify({"error": str(e)}), 500

@routes.route("/generate_hashing", methods=["POST"])
def handle_generate_hashing():
    try:
        data = request.json
        hashing_type = data.get("hashingType")
        
        if not hashing_type:
            return jsonify({"error": "Tipo de hashing não especificado"}), 400
            
        image_base64 = generate_hashing_image(hashing_type)
        return jsonify({"image": image_base64})
        
    except Exception as e:
        print(f"❌ Erro ao gerar hashing: {str(e)}")
        return jsonify({"error": str(e)}), 500

@routes.route("/generate_list", methods=["POST"])
def handle_generate_list():
    data = request.json
    list_type = data.get("listType")
    
    if list_type in ["move_to_front", "transpose"]:
        result = auto_list_operation(
            list_type=list_type,
            operation=data.get("operation"),
            value=data.get("value"),
            items=data.get("items"),
            size=data.get("size", 10)
        )
    elif list_type == "skip_list":
        result = skip_list_operation(
            operation=data.get("operation"),
            search_value=data.get("search_value"),
            insert_values=data.get("insert_values"),
            max_level=data.get("max_level", 4)
        )
    else:
        return jsonify({"error": "Invalid list type"}), 400
        
    return jsonify(result)