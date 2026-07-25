import os
import pickle
import numpy as np
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Load the pickle model
MODEL_PATH = "decision_regrassion_model_.pkl"

def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    return None

model = load_model()

# Animated Glassmorphism UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Regression Predictor</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --card-bg: rgba(255, 255, 255, 0.12);
            --card-border: rgba(255, 255, 255, 0.25);
            --input-bg: rgba(255, 255, 255, 0.08);
            --text-color: #ffffff;
            --accent-color: #00f2fe;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Poppins', sans-serif;
        }

        body {
            min-height: 100vh;
            background: linear-gradient(-45deg, #0f172a, #1e1b4b, #311042, #020617);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            color: var(--text-color);
            overflow-x: hidden;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .container {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 40px;
            width: 100%;
            max-width: 650px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
            animation: floatIn 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            position: relative;
        }

        @keyframes floatIn {
            from {
                opacity: 0;
                transform: translateY(30px) scale(0.95);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        h2 {
            font-weight: 700;
            font-size: 2rem;
            text-align: center;
            margin-bottom: 8px;
            background: linear-gradient(90deg, #00f2fe, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        p.subtitle {
            text-align: center;
            font-size: 0.95rem;
            opacity: 0.8;
            margin-bottom: 30px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        label {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            opacity: 0.9;
        }

        input, select {
            width: 100%;
            padding: 12px 16px;
            background: var(--input-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            color: #fff;
            font-size: 0.95rem;
            outline: none;
            transition: all 0.3s ease;
        }

        option {
            background-color: #1e1b4b;
            color: #fff;
        }

        input:focus, select:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
            background: rgba(255, 255, 255, 0.15);
        }

        .btn-submit {
            grid-column: 1 / -1;
            margin-top: 15px;
            padding: 15px;
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            border: none;
            border-radius: 12px;
            color: #0f172a;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 8px 25px rgba(0, 242, 254, 0.3);
        }

        .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(0, 242, 254, 0.5);
        }

        .btn-submit:active {
            transform: translateY(0);
        }

        .result-box {
            margin-top: 30px;
            padding: 20px;
            background: rgba(0, 242, 254, 0.1);
            border: 1px solid var(--accent-color);
            border-radius: 16px;
            text-align: center;
            animation: pulseIn 0.5s ease-out;
            display: {% if prediction is not none %}block{% else %}none{% endif %};
        }

        @keyframes pulseIn {
            0% { opacity: 0; transform: scale(0.9); }
            100% { opacity: 1; transform: scale(1); }
        }

        .result-title {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.8;
        }

        .result-value {
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--accent-color);
            margin-top: 5px;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>Medical Cost Prediction</h2>
    <p class="subtitle">Decision Tree Regression Model</p>

    <form action="/predict" method="POST" class="form-grid">
        <div class="input-group">
            <label for="age">Age</label>
            <input type="number" id="age" name="age" min="1" max="100" placeholder="e.g. 28" required value="{{ request.form.get('age', '') }}">
        </div>

        <div class="input-group">
            <label for="sex">Sex</label>
            <select id="sex" name="sex" required>
                <option value="1" {% if request.form.get('sex') == '1' %}selected{% endif %}>Male</option>
                <option value="0" {% if request.form.get('sex') == '0' %}selected{% endif %}>Female</option>
            </select>
        </div>

        <div class="input-group">
            <label for="bmi">BMI</label>
            <input type="number" step="0.1" id="bmi" name="bmi" placeholder="e.g. 24.5" required value="{{ request.form.get('bmi', '') }}">
        </div>

        <div class="input-group">
            <label for="children">Children</label>
            <input type="number" id="children" name="children" min="0" max="10" placeholder="e.g. 0" required value="{{ request.form.get('children', '') }}">
        </div>

        <div class="input-group">
            <label for="smoker">Smoker</label>
            <select id="smoker" name="smoker" required>
                <option value="1" {% if request.form.get('smoker') == '1' %}selected{% endif %}>Yes</option>
                <option value="0" {% if request.form.get('smoker') == '0' %}selected{% endif %}>No</option>
            </select>
        </div>

        <div class="input-group">
            <label for="region">Region</label>
            <select id="region" name="region" required>
                <option value="0" {% if request.form.get('region') == '0' %}selected{% endif %}>Southwest</option>
                <option value="1" {% if request.form.get('region') == '1' %}selected{% endif %}>Southeast</option>
                <option value="2" {% if request.form.get('region') == '2' %}selected{% endif %}>Northwest</option>
                <option value="3" {% if request.form.get('region') == '3' %}selected{% endif %}>Northeast</option>
            </select>
        </div>

        <button type="submit" class="btn-submit">Predict Expense</button>
    </form>

    <div class="result-box">
        <div class="result-title">Predicted Insurance Cost</div>
        <div class="result-value">
            {% if prediction is not none %}
                ${{ "%.2f"|format(prediction) }}
            {% endif %}
        </div>
    </div>
</div>

</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE, prediction=None)

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return "Model file not found. Ensure 'decision_regrassion_model_.pkl' is in the root directory.", 500

    try:
        # Extract features (6 expected inputs according to model metadata)
        age = float(request.form.get("age", 0))
        sex = float(request.form.get("sex", 0))
        bmi = float(request.form.get("bmi", 0))
        children = float(request.form.get("children", 0))
        smoker = float(request.form.get("smoker", 0))
        region = float(request.form.get("region", 0))

        features = np.array([[age, sex, bmi, children, smoker, region]])
        prediction_val = model.predict(features)[0]

        return render_template_string(HTML_TEMPLATE, prediction=prediction_val)
    except Exception as e:
        return f"Prediction error: {str(e)}", 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
