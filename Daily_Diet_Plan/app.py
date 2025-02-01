from flask import Flask, request, jsonify
from database import db
from models.meal import Meal

app = Flask(__name__) #Cria app atraves do Flask
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://user:password@localhost/daily_diet" #Cria o banco de dados

db.init_app(app) #Inicializa o app

@app.route("/meal", methods=["POST"])
def createMeal():
    data = request.json

    name = data.get("name")
    description = data.get("description")
    dateTime = data.get("date_time")
    inDiet = data.get("in_diet")


    if name and description and dateTime and inDiet:
        meal = Meal(name=name, description=description, dateTime=dateTime, inDiet=bool(inDiet))
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Refeição cadastrada com sucesso."})

    return jsonify({"message": "Dados inválidos para refeição."}), 400

@app.route("/meal/<int:id_meal>", methods=["PUT"])
def updateMeal(id_meal):
    data = request.json
    meal = Meal.query.get(id_meal)

    # Verifica se a refeição existe e se todos os campos estão presentes no JSON
    if meal and all(key in data for key in ["name", "description", "date_time", "in_diet"]):
        meal.name = data["name"]
        meal.description = data["description"]
        meal.dateTime = data["date_time"]
        meal.inDiet = data["in_diet"]  # Agora aceita False sem problemas

        db.session.commit()

        return jsonify({"message": f"Refeição: [{meal.name}] atualizada com sucesso."})
    
    return jsonify({"message": "Refeição não encontrada ou dados inválidos."}), 404

@app.route("/meals", methods=["GET"])
def getMeals():

    meals = Meal.query.all()  # Busca todas as refeições no banco
    if meals:
        meals_list = [{
                "name": meal.name,
                "description": meal.description,
                "date_time": meal.dateTime,
                "in_diet": meal.inDiet
            }
            for meal in meals
        ]
        return jsonify(meals_list)
    
    return jsonify({"message": "Nenhuma refeição foi encontrada."})  

@app.route("/meal/<int:id_meal>", methods=["GET"])
def getMeal(id_meal):
    
    meal = Meal.query.get(id_meal)

    if meal:
        mealInfo = [{
            "name": meal.name,
            "description": meal.description,
            "date_time": meal.dateTime,
            "in_diet": meal.inDiet
        }]

        return jsonify(mealInfo)
    
    return jsonify({"message": "Refeição não encontrada."})  

@app.route("/meal/<int:id_meal>", methods=["DELETE"])
def deleteMeal(id_meal):
    meal = Meal.query.get(id_meal)

    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": "Refeição deletada com sucesso."})
    
    return jsonify({"message": "Refeição não encontrada."})  
#Faz a aplicação rodar
if __name__ == "__main__":
    app.run(debug=True)