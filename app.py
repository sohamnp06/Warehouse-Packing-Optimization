from flask import Flask, render_template, request, redirect
from models import (
    init_db,
    add_item,
    get_active_items,
    clear_active_items,
    get_history_items
)
from knapsack import fractional_knapsack, knapsack_01

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    items = get_active_items()
    return render_template('index.html', items=items)

@app.route('/add_item', methods=['POST'])
def add_item_route():
    name = request.form['name']
    weight = float(request.form['weight'])
    profit = float(request.form['profit'])
    add_item(name, weight, profit)
    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear_active_route():
    clear_active_items()
    return redirect('/')

@app.route('/compute', methods=['POST'])
def compute():
    capacity = float(request.form['capacity'])
    items = get_active_items()

    if not items:
        return "<h2>No active items to compute. Please add items first.</h2><a href='/'>Back to Home</a>"

    frac_profit, frac_items = fractional_knapsack(items, capacity)
    int_profit, int_items = knapsack_01(items, int(capacity))

    # Recommendation considering capacity
    if int_profit >= frac_profit:
        recommendation = "0/1 Knapsack is feasible and respects capacity — use this if items cannot be divided."
    else:
        recommendation = "Fractional Knapsack gives higher theoretical profit if items can be divided, but actual capacity is respected only in 0/1 Knapsack.Better use 0/1 Knapsack"

    return render_template(
        'result.html',
        frac_profit=round(frac_profit, 2),
        frac_items=frac_items,
        int_profit=int_profit,
        int_items=int_items,
        recommendation=recommendation
    )

@app.route('/view_active')
def view_active():
    items = get_active_items()
    if not items:
        return "<h2>No active items in the database.</h2><a href='/'>Back to Home</a>"
    html = "<h2>Active Items:</h2><ul>"
    for item in items:
        html += f"<li>{item['name']} - Weight: {item['weight']}, Profit: {item['profit']}</li>"
    html += "</ul><a href='/'>Back to Home</a>"
    return html

@app.route('/history')
def view_history():
    items = get_history_items()
    if not items:
        return "<h2>No previous items.</h2><a href='/'>Back to Home</a>"
    html = "<h2>All Previous Items:</h2><ul>"
    for item in items:
        html += f"<li>{item['name']} - Weight: {item['weight']}, Profit: {item['profit']} (Added on: {item['added_on']})</li>"
    html += "</ul><a href='/'>Back to Home</a>"
    return html

if __name__ == '__main__':
    app.run(debug=True)
