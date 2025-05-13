# faj_Inventory_Management_OOP
# Inventory Management System - Assignment Report

## Assignment Summary

This assignment presents the design and implementation of an **Inventory Management System** using **Object-Oriented Programming (OOP)** in Python. The objective is to manage multiple product types, perform essential inventory operations like sales and restocking, and preserve data using JSON files. The system reflects real-world scenarios and showcases strong OOP design principles including abstraction, encapsulation, inheritance, and polymorphism.

---

## Assignment Objectives

* Develop a reusable abstract class structure for different product categories.
* Implement an inventory handler to manage add, remove, search, sell, and restock functionalities.
* Enable persistent data storage through JSON serialization.
* Ensure robust exception handling for common user and data errors.
* Provide a user-friendly CLI-based interaction system.

---

## Core Components

### 1. Abstract Base Class: `Product`

Defines a generalized product blueprint with shared attributes and behaviors for all subclasses.

**Encapsulated Attributes:**

* `_product_id`
* `_name`
* `_price`
* `_quantity_in_stock`

**Methods:**

* `restock(amount)` - Abstract
* `sell(quantity)` - Abstract
* `get_total_value()` - Calculates product value as price × stock
* `__str__()` - Returns a readable description of the product

### 2. Specialized Product Subclasses

Each subclass extends the `Product` base class with specific features:

#### Electronics

* Extra attributes: `warranty_years`, `brand`
* Custom `__str__()` output

#### Grocery

* Extra attribute: `expiry_date`
* Method: `is_expired()` to determine expired items
* Custom `__str__()` output

#### Clothing

* Extra attributes: `size`, `material`
* Custom `__str__()` output

### 3. Inventory Class

Serves as the controller for product management and stock operations.

**Responsibilities:**

* Add and remove products
* Search products by name or type
* List all inventory items
* Sell and restock items
* Compute total inventory value
* Automatically remove expired grocery products

---

## Additional Features

### JSON File Operations

* `save_to_file(filename)` stores the complete inventory
* `load_from_file(filename)` reconstructs inventory with all subclass details

### Custom Exceptions

* Attempting to sell more than available quantity
* Duplicate product IDs during addition
* Invalid or corrupted data file handling

### Command-Line Interface (CLI)

A simple interactive menu that lets users:

* Add a product
* Sell a product
* Search/view inventory
* Save/load inventory
* Exit

---

## Learning Outcomes

* Practical understanding of OOP fundamentals in Python
* Hands-on experience with class hierarchies and method overriding
* Real-world simulation using abstract base classes and polymorphism
* Working with JSON for file I/O and data serialization
* Implementing error-proof, scalable logic in command-line applications

---

## Tools & Technologies

* Python 3.x
* `abc` module for abstraction
* `json` module for file handling
* `datetime` for managing product expiration

---

## Conclusion

This assignment demonstrates a comprehensive use of object-oriented programming to design a functional and scalable inventory system. It incorporates structured logic, modular design, real-time data manipulation, and robust exception handling. It serves as an excellent example of applying Python programming in solving practical business problems.

---
