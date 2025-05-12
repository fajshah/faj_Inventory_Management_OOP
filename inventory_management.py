
import json
from abc import ABC, abstractmethod
from datetime import datetime

class Product(ABC):
    def __init__(self, product_id, name, price, quantity_in_stock):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_in_stock = quantity_in_stock

    @abstractmethod
    def restock(self, amount):
        pass

    @abstractmethod
    def sell(self, quantity):
        pass

    def get_total_value(self):
        return self._price * self._quantity_in_stock

    def __str__(self):
        return f"ID: {self._product_id}, Name: {self._name}, Price: ${self._price:.2f}, Stock: {self._quantity_in_stock}"

class Electronics(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, warranty_years, brand):
        super().__init__(product_id, name, price, quantity_in_stock)
        self.warranty_years = warranty_years
        self.brand = brand

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if quantity > self._quantity_in_stock:
            raise ValueError("Not enough stock")
        self._quantity_in_stock -= quantity

    def __str__(self):
        return f"{super().__str__()}, Brand: {self.brand}, Warranty: {self.warranty_years} yrs"

class Grocery(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, expiry_date):
        super().__init__(product_id, name, price, quantity_in_stock)
        self.expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")

    def is_expired(self):
        return datetime.now() > self.expiry_date

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if self.is_expired():
            raise ValueError("Cannot sell expired product")
        if quantity > self._quantity_in_stock:
            raise ValueError("Not enough stock")
        self._quantity_in_stock -= quantity

    def __str__(self):
        status = "Expired" if self.is_expired() else "Valid"
        return f"{super().__str__()}, Expiry: {self.expiry_date.date()} ({status})"

class Clothing(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, size, material):
        super().__init__(product_id, name, price, quantity_in_stock)
        self.size = size
        self.material = material

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if quantity > self._quantity_in_stock:
            raise ValueError("Not enough stock")
        self._quantity_in_stock -= quantity

    def __str__(self):
        return f"{super().__str__()}, Size: {self.size}, Material: {self.material}"

class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product):
        if product._product_id in self._products:
            raise ValueError("Duplicate product ID")
        self._products[product._product_id] = product

    def remove_product(self, product_id):
        if product_id not in self._products:
            raise ValueError("Product not found")
        del self._products[product_id]

    def search_by_name(self, name):
        return [p for p in self._products.values() if name.lower() in p._name.lower()]

    def search_by_type(self, product_type):
        return [p for p in self._products.values() if isinstance(p, product_type)]

    def list_all_products(self):
        return list(self._products.values())

    def sell_product(self, product_id, quantity):
        if product_id not in self._products:
            raise ValueError("Product not found")
        self._products[product_id].sell(quantity)

    def restock_product(self, product_id, quantity):
        if product_id not in self._products:
            raise ValueError("Product not found")
        self._products[product_id].restock(quantity)

    def total_inventory_value(self):
        return sum(p.get_total_value() for p in self._products.values())

    def remove_expired_products(self):
        for pid in list(self._products):
            product = self._products[pid]
            if isinstance(product, Grocery) and product.is_expired():
                del self._products[pid]

    def save_to_file(self, filename):
        data = []
        for p in self._products.values():
            obj = {
                "type": type(p).__name__,
                "product_id": p._product_id,
                "name": p._name,
                "price": p._price,
                "quantity_in_stock": p._quantity_in_stock
            }
            if isinstance(p, Electronics):
                obj.update({"warranty_years": p.warranty_years, "brand": p.brand})
            elif isinstance(p, Grocery):
                obj.update({"expiry_date": p.expiry_date.strftime("%Y-%m-%d")})
            elif isinstance(p, Clothing):
                obj.update({"size": p.size, "material": p.material})
            data.append(obj)
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename):
        self._products.clear()
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for item in data:
                    t = item["type"]
                    if t == "Electronics":
                        p = Electronics(item["product_id"], item["name"], item["price"],
                                        item["quantity_in_stock"], item["warranty_years"], item["brand"])
                    elif t == "Grocery":
                        p = Grocery(item["product_id"], item["name"], item["price"],
                                    item["quantity_in_stock"], item["expiry_date"])
                    elif t == "Clothing":
                        p = Clothing(item["product_id"], item["name"], item["price"],
                                     item["quantity_in_stock"], item["size"], item["material"])
                    else:
                        raise ValueError(f"Unknown product type: {t}")
                    self._products[p._product_id] = p
        except Exception as e:
            print("Failed to load file:", e)

def main():
    inventory = Inventory()
    while True:
        print("\n--- Inventory Management ---")
        print("1. Add Product")
        print("2. Sell Product")
        print("3. Restock Product")
        print("4. List All Products")
        print("5. Search by Name")
        print("6. Search by Type")
        print("7. Remove Expired Groceries")
        print("8. Show Total Inventory Value")
        print("9. Save Inventory")
        print("10. Load Inventory")
        print("0. Exit")
        choice = input("Enter choice: ")
        try:
            if choice == "1":
                t = input("Product type (electronics/grocery/clothing): ").lower()
                pid = input("Product ID: ")
                name = input("Name: ")
                price = float(input("Price: "))
                stock = int(input("Quantity in stock: "))
                if t == "electronics":
                    brand = input("Brand: ")
                    warranty = int(input("Warranty (years): "))
                    p = Electronics(pid, name, price, stock, warranty, brand)
                elif t == "grocery":
                    expiry = input("Expiry date (YYYY-MM-DD): ")
                    p = Grocery(pid, name, price, stock, expiry)
                elif t == "clothing":
                    size = input("Size: ")
                    material = input("Material: ")
                    p = Clothing(pid, name, price, stock, size, material)
                else:
                    print("Invalid type.")
                    continue
                inventory.add_product(p)
                print("Product added successfully.")
            elif choice == "2":
                pid = input("Product ID: ")
                qty = int(input("Quantity to sell: "))
                inventory.sell_product(pid, qty)
                print("Sold successfully.")
            elif choice == "3":
                pid = input("Product ID: ")
                qty = int(input("Quantity to restock: "))
                inventory.restock_product(pid, qty)
                print("Restocked successfully.")
            elif choice == "4":
                for p in inventory.list_all_products():
                    print(p)
            elif choice == "5":
                name = input("Search name: ")
                results = inventory.search_by_name(name)
                for p in results:
                    print(p)
            elif choice == "6":
                t = input("Type to search (electronics/grocery/clothing): ").lower()
                class_map = {
                    "electronics": Electronics,
                    "grocery": Grocery,
                    "clothing": Clothing
                }
                if t in class_map:
                    for p in inventory.search_by_type(class_map[t]):
                        print(p)
                else:
                    print("Invalid type.")
            elif choice == "7":
                inventory.remove_expired_products()
                print("Expired groceries removed.")
            elif choice == "8":
                print(f"Total Inventory Value: ${inventory.total_inventory_value():.2f}")
            elif choice == "9":
                fname = input("Filename to save: ")
                inventory.save_to_file(fname)
                print("Saved.")
            elif choice == "10":
                fname = input("Filename to load: ")
                inventory.load_from_file(fname)
                print("Loaded.")
            elif choice == "0":
                print("Exiting...")
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
