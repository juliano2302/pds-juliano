# ==========================================
# ROTAS DE PETS REESCRITAS COM ORM
# ==========================================

# 1. Listar todos os pets (com filtro opcional por dono_id)
@app.route("/pets", methods=["GET"])
def listar_pets():
    dono_id = request.args.get("dono_id")

    if dono_id:
        try:
            dono_id = int(dono_id)
            pets = Pet.query.filter_by(dono_id=dono_id).all()
        except ValueError:
            return jsonify({"erro": "dono_id deve ser um numero inteiro"}), 400
    else:
        pets = Pet.query.all()

    return jsonify([pet.to_dict() for pet in pets])


# 2. Buscar um pet por ID
@app.route("/pets/<int:pet_id>", methods=["GET"])
def buscar_pet(pet_id):
    pet = db.session.get(Pet, pet_id)

    if pet is None:
        return jsonify({"erro": "Pet nao encontrado"}), 404

    return jsonify(pet.to_dict())


# 3. Cadastrar um pet
@app.route("/pets", methods=["POST"])
def criar_pet():
    dados = request.json

    campos_obrigatorios = ["nome", "especie", "idade", "dono_id"]
    if not dados or any(campo not in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Informe nome, especie, idade e dono_id"}), 400

    # Desafio: verificar se o dono realmente existe no banco
    dono = db.session.get(Dono, dados["dono_id"])
    if dono is None:
        return jsonify({"erro": "Dono nao encontrado"}), 404

    novo_pet = Pet(
        nome=dados["nome"],
        especie=dados["especie"],
        idade=dados["idade"],
        dono_id=dados["dono_id"]
    )

    db.session.add(novo_pet)
    db.session.commit()

    return jsonify(novo_pet.to_dict()), 201


# 4. Atualizar um pet
@app.route("/pets/<int:pet_id>", methods=["PUT"])
def atualizar_pet(pet_id):
    dados = request.json

    campos_obrigatorios = ["nome", "especie", "idade", "dono_id"]
    if not dados or any(campo not in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Informe nome, especie, idade e dono_id"}), 400

    pet = db.session.get(Pet, pet_id)
    if pet is None:
        return jsonify({"erro": "Pet nao encontrado"}), 404

    # Verifica se o novo dono_id informado existe
    dono = db.session.get(Dono, dados["dono_id"])
    if dono is None:
        return jsonify({"erro": "Dono nao encontrado"}), 404

    pet.nome = dados["nome"]
    pet.especie = dados["especie"]
    pet.idade = dados["idade"]
    pet.dono_id = dados["dono_id"]

    db.session.commit()

    return jsonify(pet.to_dict())


# 5. Remover um pet
@app.route("/pets/<int:pet_id>", methods=["DELETE"])
def remover_pet(pet_id):
    pet = db.session.get(Pet, pet_id)

    if pet is None:
        return jsonify({"erro": "Pet nao encontrado"}), 404

    db.session.delete(pet)
    db.session.commit()

    return jsonify({"mensagem": "Pet removido com sucesso"})