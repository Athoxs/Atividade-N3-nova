from flask import Flask, jsonify, request
import os

app = Flask(__name__)
# Hercules Matheus Held Tabile 2°Semestre
# Armazenamento em MEMÓRIA
roupas = []
UPLOAD_FOLDER = "imagens_roupas"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Validation

# function authenticate
def autenticar_usuario(headers):
    token = headers.get("Authorization")
    if not token or token != "Bearer token_secreto":
        return False
    return True

# authenticate
@app.errorhandler(401)
def nao_autorizado(e):
    return jsonify({"erro": "Acesso nao autorizado. Forneça um token valido."}), 401

# error handler
@app.errorhandler(400)
def erro_bad_request(e):
    return jsonify({"erro": "Requisicao invalida. Verifique os dados enviados."}), 400

# Cadastrar as Roupas
@app.route("/roupas", methods=["POST"])
def criar_roupa():

    nova_roupa = request.json
    

    if any(roupa["id"] == nova_roupa["id"] for roupa in roupas):
        return jsonify({"erro": "Ja existe um cadastro com esse id."}), 400

    roupas.append(nova_roupa)
    return jsonify({"mensagem": "Roupa cadastrada com sucesso"}), 201

# Listar as Roupas
@app.route("/roupas", methods=["GET"])
def listar_roupas():
    return jsonify(roupas)

# Atualizar uma Roupa
@app.route("/roupas/<int:roupa_id>", methods=["PUT"])
def atualizar_roupa(roupa_id):
    if not autenticar_usuario(request.headers):
        return nao_autorizado(401)

    dados_atualizados = request.json

    for roupa in roupas:
        if roupa["id"] == roupa_id:
            roupa.update(dados_atualizados)
            return jsonify({"mensagem": "Roupa atualizada com sucesso!"})

    return jsonify({"erro": "Roupa nao encontrada"}), 404

# Deletar uma Roupa
@app.route("/roupas/<int:roupa_id>", methods=["DELETE"])
def deletar_roupa(roupa_id):
    if not autenticar_usuario(request.headers):
        return nao_autorizado(401)

    global roupas
    roupas = [roupa for roupa in roupas if roupa["id"] != roupa_id]
    return jsonify({"mensagem": "Roupa deletada com sucesso."})

# Consulta de Roupas
@app.route("/roupas/buscar", methods=["GET"])
def buscar_roupa_por_nome():
    nome = request.args.get("nome", "").lower()
    resultados = [roupa for roupa in roupas if nome in roupa["nome"].lower()]
    return jsonify(resultados)

@app.route("/roupas/categoria", methods=["GET"])
def filtrar_por_categoria():
    categoria = request.args.get("categoria", "").lower()
    resultados = [roupa for roupa in roupas if roupa.get("categoria", "").lower() == categoria]
    return jsonify(resultados)

@app.route("/roupas/destaque", methods=["GET"])
def listar_roupas_em_destaque():
    destaques = [roupa for roupa in roupas if roupa.get("destaque", False)]
    return jsonify(destaques)

# Inicializar a aplicação
if __name__ == "__main__":
    app.run(debug=True)
