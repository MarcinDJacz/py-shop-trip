from app.customer import Customer
from app.shop import Shop
import json
import math
import datetime


def shop_trip() -> None:
    with open("app/config.json", "r") as file:
        data = json.load(file)
    fuel_price = data["FUEL_PRICE"]
    customers = [Customer(*(list(one_customer.values())))
                 for one_customer in data["customers"]]
    shops = [Shop(*(list(one_shop.values()))) for one_shop in data["shops"]]

    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")
        customer_x, customer_y = customer.location
        cost = 0
        choose_shop = ""
        total_cost = 0
        for shop in shops:
            shop_x, shop_y = shop.location
            distance = round(
                math.sqrt(
                    pow((shop_x - customer_x), 2)
                    + pow((shop_y - customer_y), 2)), 2)
            cost_fuel = ((distance * customer.car["fuel_consumption"] / 100)
                         * fuel_price)
            cost_products = [shop.products[key] * value
                             for key, value in customer.product_cart.items()]
            cost_actual = round(cost_fuel * 2 + sum(cost_products), 2)
            print(f"{customer.name}'s trip to {shop.name} costs {cost_actual}")
            if not cost or cost_actual < cost:
                choose_shop = shop
                cost = cost_actual
                total_cost = sum(cost_products)
        if customer.money - total_cost >= 0:
            print(f"{customer.name} rides to {choose_shop.name}")
            print("")
            print(f"Date: {datetime.datetime.now()}")
            print(f"Thanks, {customer.name}, for your purchase!")
            print("You have bought:")
            for key, value in customer.product_cart.items():
                print(f"{value} {key}s for"
                      f" {value * choose_shop.products[key]} dollars")
            print(f"Total cost is {total_cost} dollars")
            print("See you again!")
            print("")
            print(f"{customer.name} rides home")
            customer.money -= total_cost
            print(f"{customer.name} now has {customer.money} dollars")
            print("")
        else:
            print(f"{customer.name} doesn't have"
                  f" enough money to make a purchase in any shop")
