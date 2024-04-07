## ----------------------------- Imports -----------------------------
from pymongo import MongoClient 
## pymongo version: # 4.6.1
import json

## ----------------------------- Setup -----------------------------
## read Configuration
def read_configuration(file_name= "config.json"):
    with open(file_name, mode="r") as file:
        config = json.load(file)
    return config

config = read_configuration()
MONGO_HOST = config["host"]
MONGO_PORT = config["port"]
DB_NAME = config["db_name"]
client = MongoClient(MONGO_HOST, MONGO_PORT)
# client = MongoClient("mongodb://localhost:27017")
DB = client[DB_NAME]

## ----------------------------- Defining Schemas ----------------------------- 
menu_items_schema = """
    db.createCollection("MenuItems", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      additionalProperties: false,
      required: ["name", "price", "category", "ingredients"],
      properties: {
        _id: {}, // Explicitly allowing the _id field
        name: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        price: {
          bsonType: "double",
          description: "must be a double and is required"
        },
        category: {
          bsonType: "string",
          description: "must be an string and is required"
        },
        ingredients: {
          bsonType: "string",
          description: "must be a string and is required"
        }
      }
    }
  }
  validationLevel: "strict"
});
"""

customers_schema = """
    db.createCollection("Customers", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["ID", "name", "phone_number"],
      properties: {
        ID: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        
        name: {
          bsonType: "string",
          description: "must be an stirng and is required"
        },
        phone_number: {
          bsonType: "string",
          description: "must be a string and is required"
        }
      }
    }
  }
});
"""

orders_schema = """
    db.createCollection("Orders", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["order_ID", "customer_ID", "item1"],
      properties: {
        order_ID: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        customer_ID: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        item1: {
          bsonType: "string",
          description: "a string representing menu item's name"
        }
      }
    }
  }
});
"""

feedback_schema ="""
    db.createCollection("CustomerFeedback", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      additionalProperties: false,
      required: ["customer_ID", "feedback"],
      properties: {
        _id: {}, // Explicitly allowing the _id field
        customer_ID: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        
        feedback: {
          bsonType: "string",
          description: "must be a string and is required"
        }
      }
    }
  }
  validationLevel: "strict"
});
"""
## ----------------------------- Creating Collections or Connecting to Collections ----------------------------- 
try:
    MENU_ITEMS = DB.create_collection("MenuItems", validator= menu_items_schema)
except:
    MENU_ITEMS = DB["MenuItems"]

try:
    ORDERS = DB.create_collection("Orders", validator= orders_schema)
except:
    ORDERS = DB["Orders"]

try:
    CUSTOMERS = DB.create_collection("Customers", validator= customers_schema)
except:
    CUSTOMERS = DB["Customers"]
CUSTOMERS.create_index("ID", unique= True)

try:
    CUSTOMER_FEEDBACK = DB.create_collection("CustomerFeedback", validator= feedback_schema)
except:
    CUSTOMER_FEEDBACK = DB["CustomerFeedback"]

## ----------------------------- Menu Items Management -----------------------------
def add_menu_item():
    name = input("Menu Item's Name: ")
    ## Checking if the input name is already exists
    menu_item = MENU_ITEMS.find_one({"name": name})
    if menu_item:
        print("The requested menu item already exists!")
        return
    try:
        price = float(input("Menu Item's Price: "))
    except ValueError as e:
        print(e)
        return
    category = input("Menu Item's Category: ")
    ingredients = input("Menu Item's Ingredients: ")
    ## Constructing the dictionary
    item = {
        "name": name,
        "price": price,
        "category": category,
        "ingredients": ingredients
    }
    ## Executing MongoDB command
    insert_one_result = MENU_ITEMS.insert_one(item)
    if insert_one_result.acknowledged:
        print("New Item is added!")
    else:
        print("New item cannot be added!")


def view_menu_items():
    menu_items = MENU_ITEMS.find()
    menu_items = list(menu_items)
    if len(menu_items) == 0:
        print("No menu item have been found!!")
    else:
        print("-"*10, " Menu Items ", "-"*10)
    for menu_item in menu_items:
        output = []
        for k, v in menu_item.items():
            if k != "_id":
                output.append(f"{k}: {v}")
        print(", ".join(output))
            

def update_menu_item():
    pre_name = input("Menu Item's Name (to update): ")
    ## Checking if the input name is in the menu items
    menu_item = MENU_ITEMS.find_one({"name": pre_name})
    if not menu_item:
        print("The requested menu item does not exist!")
        return
    ## Retrieving the previous values
    pre_price = menu_item["price"]
    pre_category = menu_item["category"]
    pre_ingred = menu_item["ingredients"]
    ## Getting new values
    new_price = input("New Menu Item's Price (press Enter to skip): ") or pre_price
    if not new_price: # the user entered a different key instead of pressing "Enter"
        try:
            new_price = float(new_price)
        except ValueError as e:
            print(f"Invalid Numerical Value for `price`: {e}")
            return
    new_category = input("New Menu Item's Category (press Enter to skip): ") or pre_category
    new_ingred = input("New Menu Item's Ingredients (press Enter to skip): ") or pre_ingred
    ## Updaing the values of menu item (The name cannot be updated)
    update_result = MENU_ITEMS.update_one({"name": pre_name}, 
                                          {"$set": {"price": new_price, "category":new_category, "ingredients": new_ingred}})
    if update_result.acknowledged:
        print("The item has been successfully updated.")
    else:
        print("The item cannot be updated!")


def delete_menu_item():
    """
    The "name" property of the MenuItems Collection is linked to the items properties in the Orders Collection. 
    However, from a logical standpoint, it is generally unnecessary to modify the values of items in the Orders Collection. 
    It is expected and considered normal to have past orders that include previously available menu items.
    """
    name = input("Menu Item's Name (to delete): ")
    ## Checking if the input name is in the menu items
    menu_item = MENU_ITEMS.find_one({"name": name})
    if not menu_item:
        print("The requested menu item does not exist!")
        return
    ## Removing the menu item
    delete_result = MENU_ITEMS.delete_one({"name": name})
    if delete_result.acknowledged:
        print("The item has been successfully removed.")
    else:
        print("The item cannot be removed.")

## ----------------------------- Customers Management -----------------------------
def add_customer():
    ## Generating a unique customer ID 
    customer_ids = CUSTOMERS.find({}, {"ID": 1, "_id": 0})
    customer_ids = list(customer_ids) # a list of dictionaries
    if not customer_ids:
        customer_id = "1111"
    else:
        customer_ids = [d.get("ID") for d in customer_ids] # a list of strs
        customer_id = str(max(list(map(lambda x: int(x), customer_ids))) + 1)
    ## Getting Customer Information
    name = input("The customer's name: ")
    phone_num = input("The customer's phone number: ")
    ## Getting additional information 
    additional_info = {}
    while True:
        key = input("If you would like to add any additional information, please enter the corresponding label (Press enter to skip): ")
        if not key:
            break
        if key == "ID":
            print("The customer ID cannot be modified.")
            break
        value = input(f"Please enter the value for the label '{key}': ")
        if not value:
            break
        additional_info[key] = value
    ## Constructing the dictionary
    cust = {
        "ID": customer_id,
        "name": name,
        "phone_number": phone_num
    }
    cust.update(additional_info)
    ## Executing MongoDB command
    insert_one_result = CUSTOMERS.insert_one(cust)
    if insert_one_result.acknowledged:
        print(f"New customer is added. Customer ID: {customer_id}")
    else:
        print("Cannot add new customer!")


def update_customer_profile():
    id_ = input("The customer's ID: ")
    ## Checking if the input ID is in the customers
    customer = CUSTOMERS.find_one({"ID": id_})
    if not customer: # NoneType or dict
        print("The requested ID does not exist!")
        return
    ## Display the present customer information
    print("-"*10, " Present Customer Information ", "-"*10)
    properties = []
    for k, v in customer.items():
        if k != "_id":
            properties.append(f"{k}: {v}")
    print(", ".join(properties))
    ##
    update_info = {}
    while True:
        key = input("Please enter the label for which you would like to update its value (Press enter to skip): ")
        if not key:
            break
        if key == "ID":
            print("The customer ID cannot be modified.")
            break
        value = input(f"Please enter the value for the label '{key}': ")
        if not value:
            break
        update_info[key] = value
    
    update_result = CUSTOMERS.update_one({"ID": id_}, {"$set": update_info})
    if update_result.acknowledged:
        print("The customer's record has been successfully updated.")
    else:
        print("The customer's record cannot be updated!")
 

def view_customer_details():
    id_ = input("The customer's ID: ")
    ## Checking if the input ID is in the customers
    customer = CUSTOMERS.find_one({"ID": id_})
    if not customer: # NoneType or dict
        print("The requested ID does not exist!")
        return
    ## printing the customer's information
    properties = []
    for k, v in customer.items():
        if k != "_id":
            properties.append(f"{k}: {v}")
    print("-"*10, " Customer's Details ", "-"*10)
    print(", ".join(properties))


def remove_customer():
    """
    In order to maintain dependency between collections, prior to deleting a customer record with a specific ID, 
    we modify the customer_id in both Orders and CustomerFeedbacks collections that share the same value as the ID.
    The value '0000' assigned to customer_id signifies a deleted customer account.
    """
    id_ = input("The customer's ID (to delete): ")
    ## Checking if the input ID is in the customers
    customer = CUSTOMERS.find_one({"ID": id_})
    if not customer:
        print("The requested customer ID does not exist!")
        return
    ## Modifying corresponding customer_id in Orders Collection
    ORDERS.update_many({"customer_ID": id_}, {"$set": {"customer_ID": "0000"}})
    ## Modifying corresponding customer_id in CustomerFeedback Collection
    CUSTOMER_FEEDBACK.update_many({"customer_ID": id_}, {"$set": {"customer_ID": "0000"}})
    ## Removing the customer
    delete_result = CUSTOMERS.delete_one({"ID": id_})
    if delete_result.acknowledged:
        print("The customer's record has been successfully removed.")
    else:
        print("The customer's record cannot be removed.")
    

def view_customers():
    customers = CUSTOMERS.find()
    customers = list(customers)
    if len(customers) == 0:
        print("No customers have been found!")    
    else:
        print("-"*10, " Customers ", "-"*10)
    for customer in customers:
        output = []
        for k, v in customer.items():
            if k != "_id":
                output.append(f"{k}: {v}")
        print(", ".join(output))

## ----------------------------- Orders Management -----------------------------
## Place an order
def place_order():
    id_ = input("The customer's ID (to order): ")
    ## Checking if the input ID is in the customers
    customer = CUSTOMERS.find_one({"ID": id_})
    if not customer:
        print("The requested customer ID does not exist!")
        return
    ## Generating a unique order ID 
    order_ids = ORDERS.find({}, {"order_ID": 1, "_id": 0})
    order_ids = list(order_ids) # a list of dictionaries
    if not order_ids:
        order_id = "1111"
    else:
        order_ids = [d.get("order_ID") for d in order_ids] # a list of strs
        order_id = str(max(list(map(lambda x: int(x), order_ids))) + 1)
    ## 
    order = {}
    order["order_ID"] = order_id
    order["customer_ID"] = id_
    ## Taking the first item of the order. The customer must order at least one menu item
    item = input("Could you please tell me your order? ")
    while True:
        ## Checking if the ordered item is in menu items
        menu_item = MENU_ITEMS.find_one({"name": item})
        if menu_item:
            break
        item = input("I apologize, but we currently do not have that item available. Would you like to consider another choice? ")
    order["item1"] = item
    ## Taking the other items
    item = input("May I kindly inquire about your next selection? (press Enter to complete the order) ")
    item_num = 2
    while True:
        if not item: ## The customer pressed Enter
            break
        ## Checking if the ordered item is in menu items
        menu_item = MENU_ITEMS.find_one({"name": item})
        if not menu_item:
            print("I apologize, but we currently do not have that item available.")
        else:
            key = "item" + str(item_num)
            order[key] = item
            item_num += 1
        item = input("Would you like to consider another choice? (press Enter to complete the order) ")
    ## Executing MongoDB insert_one
    insert_result = ORDERS.insert_one(order) 
    if insert_result.acknowledged:
        print(f"Order submitted successfully. Order ID: {order_id}")
    else:
        print("Cannot submit the order")   


## View an order
def view_order():
    order_id = input("Please enter the order ID: ")
    order = ORDERS.find_one({"order_ID": order_id})
    if not order:
        print("No orders have been found!")
    else:
        print("-"*30)
        for k,v in order.items():
            if k != "_id":
                print(f"{k}: {v}")
        

def view_all_orders():
    orders = ORDERS.find()
    orders = list(orders)
    if len(orders) == 0:
        print("No orders have been found!")    
    else:
        print("-"*10, " Orders ", "-"*10)
    for order in orders:
        output = []
        for k, v in order.items():
            if k != "_id":
                output.append(f"{k}: {v}")
        print(", ".join(output))


## Modify the order
def modify_order():
    ## To modify an order, it involves reselecting the desired menu items.
    order_id = input("The order's ID (to modify): ")
    ## Checking if the input ID is in the customers
    order = ORDERS.find_one({"order_ID": order_id})
    if not order:
        print("The requested order ID does not exist!")
        return
    ## Removing order's items
    items = {}
    for k in order.keys():
        if k != "_id" and k != "order_ID" and k!= "customer_ID":
            items[k] = ""
    ORDERS.update_one({"order_ID": order_id},{"$unset": items})
    
    ## Reselecting the desired menu items
    ## Taking the first item of the order. The customer must order at least one menu item
    m_order = {}
    item = input("Could you please tell me your order? ")
    while True:
        ## Checking if the ordered item is in menu items
        menu_item = MENU_ITEMS.find_one({"name": item})
        if menu_item:
            break
        item = input("I apologize, but we currently do not have that item available. Would you like to consider another choice? ")
    m_order["item1"] = item
    ## Taking the other items
    item = input("May I kindly inquire about your next selection? (press Enter to complete the order) ")
    item_num = 2
    while True:
        if not item: ## The customer pressed Enter
            break
        ## Checking if the ordered item is in menu items
        menu_item = MENU_ITEMS.find_one({"name": item})
        if not menu_item:
            print("I apologize, but we currently do not have that item available.")
        else:
            key = "item" + str(item_num)
            m_order[key] = item
            item_num += 1
        item = input("Would you like to consider another choice? (press Enter to complete the order) ")
    ## Executing MongoDB update_one
    update_result = ORDERS.update_one({"order_ID": order_id}, {"$set": m_order}) 
    if update_result.acknowledged:
        print(f"Order updated successfully. Order ID: {order_id}")
    else:
        print("Cannot update the order")   


## Cancel the order
def cancel_order():
    order_id = input("Please enter the order ID (to cancel): ")
    order = ORDERS.find_one({"order_ID": order_id})
    if not order:
        print("No orders have been found!")
    else:
        delete_result = ORDERS.delete_one({"order_ID": order_id})
        if delete_result:
            print(f"The order {order_id} has been cancelled.")
        else:
            print(f"The order {order_id} cannot be cancelled.")

## ----------------------------- Customer Feedbacks Management -----------------------------
def add_feedback():
    id_ = input("The customer's ID: ")
    ## Checking if the input ID is in the customers
    customer = CUSTOMERS.find_one({"ID": id_})
    if not customer: # NoneType or dict
        print("The requested ID does not exist!")
        return
    feedback = input("The customer's feedback: ")
    insert_one_result = CUSTOMER_FEEDBACK.insert_one({"customer_ID": id_, "feedback": feedback})
    if insert_one_result.acknowledged:
        print("Thank you for your feedback.")
    else:
        print("Cannot submit your feedback!")


def view_customer_feedbacks():
    id_ = input("The customer's ID: ")
    ## Checking if the input ID is in the customers
    customer = CUSTOMERS.find_one({"ID": id_})
    if not customer: # NoneType or dict
        print("The requested ID does not exist!")
        return
    ## Retrieving all feedbacks
    feedbacks = CUSTOMER_FEEDBACK.find({"customer_ID": id_})
    feedbacks = list(feedbacks)
    if len(feedbacks) == 0:
        print(f"No feedbacks have been found for customer {id_}!")    
    else:
        print("-"*10, f" Feedback(s) for Customer {id_} ", "-"*10)
    for feedback in feedbacks:
        output = []
        for k, v in feedback.items():
            if k != "_id":
                output.append(f"{k}: {v}")
        print(", ".join(output))


def view_all_feedbacks():
    feedbacks = CUSTOMER_FEEDBACK.find()
    feedbacks = list(feedbacks)
    if len(feedbacks) == 0:
        print(f"No feedbacks have been found!")    
    else:
        print("-"*10, " Feedback(s) ", "-"*10)
    for feedback in feedbacks:
        output = []
        for k, v in feedback.items():
            if k != "_id":
                output.append(f"{k}: {v}")
        print(", ".join(output))
    

## ----------------------------- Main -----------------------------
def main_menu():
    while True:
        menu_msg ="""
        \nRestaurant Management System
        ---------- Menu Operations ----------
        1. Add menu item
        2. View menu items
        3. Delete a menu item
        4. Update a menu item
        ---------- Order Operations ----------
        5. Place an order
        6. View an order
        7. Modify the order
        8. Cancel the order
        9. View all orders of the restaurant
        ---------- Customer Operations ----------
        10. Add new customer
        11. Remove a customer
        12. Update a customer
        13. View a customer's details
        14. View all customers
        ---------- Feedback Operations ----------
        15. Add a feedback
        16. View a customer's feedbacks
        17. View all feedbacks

        20. Exit
        """
        print(menu_msg)
        choice = input("Enter choice: ")

        if choice == '1':
            add_menu_item()
        elif choice == '2':
            view_menu_items()
        elif choice == '3':
            delete_menu_item()
        elif choice == '4':
            update_menu_item()

        elif choice == '5':
            place_order()
        elif choice == '6':
            view_order()
        elif choice == '7':
            modify_order()
        elif choice == '8':
            cancel_order()
        elif choice == '9':
            view_all_orders()

        elif choice == '10':
            add_customer()
        elif choice == '11':
            remove_customer()
        elif choice == '12':
            update_customer_profile()
        elif choice == '13':
            view_customer_details()
        elif choice == '14':
            view_customers()

        elif choice == '15':
            add_feedback()
        elif choice == '16':
            view_customer_feedbacks()
        elif choice == '17':
            view_all_feedbacks()

        elif choice == '20':
            break
        else:
            print("Invalid! Please try again.")

main_menu()