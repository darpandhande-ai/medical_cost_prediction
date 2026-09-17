import os
import pickle
import numpy as np
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# Load Model
MODEL_PATH = "mcp_model.pkl"
model = None

if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print(f"Warning: {MODEL_PATH} not found in the root directory.")

# Inline Glassmorphism & Animated HTML/CSS Dashboard Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Medical Cost Analytics Dashboard</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        :root[data-theme="dark"] {
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(255, 255, 255, 0.08);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --input-bg: rgba(15, 23, 42, 0.6);
            --input-border: rgba(255, 255, 255, 0.12);
            --shadow-color: rgba(0, 0, 0, 0.37);
            --accent-primary: #6366f1;
            --accent-secondary: #ec4899;
            --accent-tertiary: #06b6d4;
            --chart-grid: rgba(255, 255, 255, 0.05);
            --chart-text: #94a3b8;
        }

        :root[data-theme="light"] {
            --bg-gradient: linear-gradient(135deg, #f0f3ff 0%, #e0e7ff 50%, #f0f3ff 100%);
            --card-bg: rgba(255, 255, 255, 0.85);
            --card-border: rgba(255, 255, 255, 0.6);
            --text-main: #0f172a;
            --text-muted: #64748b;
            --input-bg: rgba(241, 245, 249, 0.8);
            --input-border: rgba(203, 213, 225, 0.8);
            --shadow-color: rgba(99, 102, 241, 0.08);
            --accent-primary: #4f46e5;
            --accent-secondary: #db2777;
            --accent-tertiary: #0891b2;
            --chart-grid: rgba(0, 0, 0, 0.05);
            --chart-text: #64748b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: var(--bg-gradient);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: var(--text-main);
            min-height: 100vh;
            padding: 2rem 1rem;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .dashboard-container {
            width: 100%;
            max-width: 1280px;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        /* Header Bar */
        .header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            padding: 1.25rem 2rem;
            border-radius: 20px;
            box-shadow: 0 20px 25px -5px var(--shadow-color);
        }

        .brand-title {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .theme-toggle-btn {
            background: var(--input-bg);
            border: 1px solid var(--input-border);
            color: var(--text-main);
            padding: 10px 16px;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .theme-toggle-btn:hover {
            transform: translateY(-2px);
            border-color: var(--accent-primary);
        }

        /* Layout Grid */
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }

        @media (min-width: 992px) {
            .dashboard-grid {
                grid-template-columns: 420px 1fr;
            }
        }

        /* Glass Cards */
        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 1.75rem;
            box-shadow: 0 20px 25px -5px var(--shadow-color);
            position: relative;
            overflow: hidden;
        }

        .glass-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), var(--accent-tertiary));
        }

        .card-title {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Form Inputs */
        .form-group {
            margin-bottom: 1.2rem;
        }

        .form-label {
            display: block;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .input-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }

        .input-icon {
            position: absolute;
            left: 14px;
            color: var(--accent-primary);
        }

        .form-control {
            width: 100%;
            padding: 12px 14px 12px 42px;
            background: var(--input-bg);
            border: 1px solid var(--input-border);
            border-radius: 12px;
            color: var(--text-main);
            font-size: 0.95rem;
            font-weight: 500;
            outline: none;
        }

        .form-control:focus {
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        .submit-btn {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 12px;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            color: #ffffff;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
            margin-top: 1rem;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            opacity: 0.95;
        }

        /* Analytics View */
        .analytics-container {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            height: 100%;
        }

        .result-banner {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            animation: pulseGlow 4s infinite alternate;
        }

        @keyframes pulseGlow {
            0% { box-shadow: 0 0 15px rgba(99, 102, 241, 0.1); }
            100% { box-shadow: 0 0 25px rgba(236, 72, 153, 0.25); }
        }

        .result-label {
            font-size: 0.9rem;
            color: var(--text-muted);
            font-weight: 600;
        }

        .result-value {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .chart-wrapper {
            position: relative;
            flex-grow: 1;
            min-height: 320px;
            width: 100%;
        }

        /* Loading Spinner Animation */
        .spinner {
            display: none;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>

    <div class="dashboard-container">
        <!-- Top Navbar -->
        <header class="header-bar">
            <div class="brand-title">
                <i class="fa-solid fa-chart-line-up"></i>
                <span>Predictive Analytics Engine</span>
            </div>
            <button class="theme-toggle-btn" onclick="toggleTheme()" id="themeBtn">
                <i class="fa-solid fa-moon"></i>
                <span id="themeBtnText">Dark Mode</span>
            </button>
        </header>

        <!-- Content Grid -->
        <main class="dashboard-grid">
            <!-- Form Input Panel -->
            <section class="glass-card">
                <h2 class="card-title">
                    <i class="fa-solid fa-sliders" style="color: var(--accent-primary)"></i>
                    Model Parameters
                </h2>
                <form id="predictionForm">
                    <div class="form-group">
                        <label class="form-label">Age</label>
                        <div class="input-wrapper">
                            <i class="fa-solid fa-user input-icon"></i>
                            <input type="number" name="age" class="form-control" value="35" required min="18" max="100">
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Sex</label>
                        <div class="input-wrapper">
                            <i class="fa-solid fa-venus-mars input-icon"></i>
                            <select name="sex" class="form-control" required>
                                <option value="1">Male (1)</option>
                                <option value="0">Female (0)</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Body Mass Index (BMI)</label>
                        <div class="input-wrapper">
                            <i class="fa-solid fa-weight-scale input-icon"></i>
                            <input type="number" step="0.1" name="bmi" class="form-control" value="28.5" required min="10" max="60">
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Children</label>
                        <div class="input-wrapper">
                            <i class="fa-solid fa-child input-icon"></i>
                            <input type="number" name="children" class="form-control" value="1" required min="0" max="10">
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Smoker</label>
                        <div class="input-wrapper">
                            <i class="fa-solid fa-smoking input-icon"></i>
                            <select name="smoker" class="form-control" required>
                                <option value="0">No (0)</option>
                                <option value="1">Yes (1)</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Region Index</label>
                        <div class="input-wrapper">
                            <i class="fa-solid fa-map-location-dot input-icon"></i>
                            <select name="region" class="form-control" required>
                                <option value="0">Northeast (0)</option>
                                <option value="1">Northwest (1)</option>
                                <option value="2">Southeast (2)</option>
                                <option value="3">Southwest (3)</option>
                            </select>
                        </div>
                    </div>

                    <button type="submit" class="submit-btn">
                        <span id="btnText">Calculate Prediction</span>
                        <div class="spinner" id="btnSpinner"></div>
                    </button>
                </form>
            </section>

            <!-- Results & Visualization Panel -->
            <section class="glass-card">
                <div class="analytics-container">
                    <h2 class="card-title">
                        <i class="fa-solid fa-chart-pie" style="color: var(--accent-secondary)"></i>
                        Analytics Output
                    </h2>

                    <div class="result-banner">
                        <div>
                            <div class="result-label">Predicted Outcome Value</div>
                            <div style="font-size: 0.8rem; color: var(--text-muted); font-weight: 500;">DecisionTreeRegressor Model Result</div>
                        </div>
                        <div class="result-value" id="predictionOutput">$0.00</div>
                    </div>

                    <div class="chart-wrapper">
                        <canvas id="featureChart"></canvas>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <script>
        let chartInstance = null;

        // Dynamic Chart Initialization
        function renderChart(predictionValue = 0) {
            const ctx = document.getElementById('featureChart').getContext('2d');
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const textColor = isDark ? '#94a3b8' : '#64748b';
            const gridColor = isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)';

            if (chartInstance) {
                chartInstance.destroy();
            }

            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Baseline Min', 'Estimated Output', 'Baseline Max'],
                    datasets: [{
                        label: 'Valuation Comparison',
                        data: [1121.87, predictionValue, 63770.42],
                        backgroundColor: [
                            'rgba(6, 182, 212, 0.65)',
                            'rgba(236, 72, 153, 0.85)',
                            'rgba(99, 102, 241, 0.65)'
                        ],
                        borderColor: [
                            '#06b6d4',
                            '#ec4899',
                            '#6366f1'
                        ],
                        borderWidth: 2,
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: (context) => ` Value: $${context.raw.toLocaleString()}`
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: { color: gridColor },
                            ticks: { color: textColor, font: { family: 'Plus Jakarta Sans', weight: '600' } }
                        },
                        y: {
                            grid: { color: gridColor },
                            ticks: { color: textColor, font: { family: 'Plus Jakarta Sans', weight: '600' } }
                        }
                    }
                }
            });
        }

        // Theme Toggle Handler
        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            
            const btnText = document.getElementById('themeBtnText');
            const btnIcon = document.querySelector('#themeBtn i');

            if (newTheme === 'dark') {
                btnText.textContent = 'Dark Mode';
                btnIcon.className = 'fa-solid fa-moon';
            } else {
                btnText.textContent = 'Light Mode';
                btnIcon.className = 'fa-solid fa-sun';
            }

            renderChart(window.lastPrediction || 0);
        }

        // Asynchronous Prediction Endpoint Form Submission
        document.getElementById('predictionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const btnText = document.getElementById('btnText');
            const btnSpinner = document.getElementById('btnSpinner');
            
            btnText.style.display = 'none';
            btnSpinner.style.display = 'block';

            const formData = new FormData(e.target);

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                if (data.status === 'success') {
                    const value = data.prediction;
                    window.lastPrediction = value;
                    document.getElementById('predictionOutput').textContent = `$${value.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
                    renderChart(value);
                } else {
                    alert('Prediction Error: ' + data.message);
                }
            } catch (err) {
                alert('Server Communication Error: ' + err.message);
            } finally {
                btnText.style.display = 'inline';
                btnSpinner.style.display = 'none';
            }
        });

        // Initial Chart Load
        renderChart(0);
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"status": "error", "message": "Model pickle file (mcp_model.pkl) was not loaded properly."})
    
    try:
        age = float(request.form.get("age", 0))
        sex = float(request.form.get("sex", 0))
        bmi = float(request.form.get("bmi", 0))
        children = float(request.form.get("children", 0))
        smoker = float(request.form.get("smoker", 0))
        region = float(request.form.get("region", 0))

        # Inputs ordered according to features: ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
        input_data = np.array([[age, sex, bmi, children, smoker, region]])
        prediction = model.predict(input_data)[0]

        return jsonify({
            "status": "success",
            "prediction": float(prediction)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
