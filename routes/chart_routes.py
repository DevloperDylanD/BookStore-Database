from flask import Blueprint
from flask_login import login_required
from models import db, Customer, Order
import matplotlib.pyplot as plt

chart_bp = Blueprint('chart', __name__)


@chart_bp.route('/chart')
@login_required
def chart():
    customers = Customer.query.all()

    labels = []
    totals = []

    for cust in customers:
        total_amount = db.session.query(db.func.sum(Order.total_amount)).filter_by(customer_id=cust.customer_id).scalar()
        labels.append(cust.name)
        totals.append(total_amount or 0)

    plt.figure(figsize=(12, 5))
    plt.bar(labels, totals)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/chart.png")
    plt.close()

    return "<img src='/static/chart.png'>"
