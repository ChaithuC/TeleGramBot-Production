# imports
import os
import telebot
from keep_alive import keep_alive
from communication import *
import re
api = os.environ['api']

#enabling Bot
bot = telebot.TeleBot(api)


# welcome message
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        """ Hello, Amigo!, Want to order pure milk or mineral water ? click /PRODUCTS to Order"""
    )


# PRODUCTS
@bot.message_handler(commands=['PRODUCTS'])
def options(PRODUCTS):
    options_msg = bot.send_message(
        PRODUCTS.chat.id, """ REPLY what You want to Order:
  Reply with 1 for Milk
  Reply with 2 for Mineral water""")
    bot.register_next_step_handler(options_msg, wish_list)


# WISH LIST
def wish_list(options_msg):
    product = options_msg.text
    if int(product) == 1:
        selected_product = "Milk"
        options_msg = bot.send_message(
            options_msg.chat.id,
            f"Your Selected Product is {selected_product}" +
            """ How many Liters:
                 
                 Reply with 1 for 1.0Liter
                 Reply with 2 for 2.0Liter
                 Reply with 3 for 3.0Liter
                 Reply with 4 for 4.0Liter
                 Reply with 5 for 5.0Liter                  
                                   .""")

        bot.register_next_step_handler(options_msg, quantity, selected_product)

    elif int(product) == 2:
        selected_product = "Mineral water"
        options_msg = bot.send_message(
            options_msg.chat.id,
            f"Your Selected Product is {selected_product}" +
            """How many Can(s):
                                     
                 Reply with 1 for 1 can
                 Reply with 2 for 2 cans
                 Reply with 3 for 3 cans
                 Reply with 4 for 4 cans
                 Reply with 5 for 5 cans
                                     """)

        bot.register_next_step_handler(options_msg, quantity, selected_product)


#Quantity
def quantity(options_msg, selected_product):
    # setting up the metric for the count
    if selected_product == "Milk":
        metric = "Liter(s)"
    elif selected_product == "Mineral water":
        metric = "can(s)"
    inputt = options_msg.text

    # parsing the Quantity
    if int(inputt) == 1:
        options_msg = bot.send_message(
            options_msg.chat.id,
            f"Selected Quantity for {selected_product} is {inputt} {metric} ,Plese enter your mobile number:"
        )
    if int(inputt) == 2:
        options_msg = bot.send_message(
            options_msg.chat.id,
            f"Selected Quantity for {selected_product} is {inputt} {metric} ,Plese enter your mobile number:"
        )
    if int(inputt) == 3:
        options_msg = bot.send_message(
            options_msg.chat.id,
            f"Selected Quantity for {selected_product} is {inputt} {metric} ,Plese enter your mobile number:"
        )
    if int(inputt) == 4:
        options_msg = bot.send_message(
            options_msg.chat.id,
            f"Selected Quantity for {selected_product} is {inputt} {metric} ,Plese enter your mobile number:"
        )
    if int(inputt) == 5:
        options_msg = bot.send_message(
            options_msg.chat.id,
            f"Selected Quantity for {selected_product} is {inputt} {metric} ,Plese enter your mobile number:"
        )

    #stepping to other function
    bot.register_next_step_handler(options_msg, FinaliseBill, selected_product,
                                   inputt, metric)


#FinaliseBill
def FinaliseBill(options_msg, selected_product, inputt, metric):
    Entered_Number = options_msg.text
    db_customer_check = test(Entered_Number)
    if db_customer_check.empty:
        new_order = (
            f"New Order Recived , Number {Entered_Number} and Product {selected_product} with {inputt} {metric}, Customer Data Not Available in Data base"
        )
        sent_response = (
            f"Your Product  {selected_product} with {inputt} {metric} is Recived! and will be delivered soon ,Seems like Your Number {Entered_Number} is not registered with us, Our Team will get back to you soon, Thanks For Ordering .. Feel Free to Give any Suggestions"
        )

        options_msg = bot.send_message(options_msg.chat.id, sent_response)
        print("new_order:", new_order)
    else:

        def removing(rg_string):
            rg_string = str(rg_string)
            for i in range(2):
                if i == 0:
                    pattern = r"[\([{})\]]"
                    mod_stringg = re.sub(pattern, '', rg_string)
                if i == 1:
                    pattern = r"dict_values"
                    mod_string = re.sub(pattern, '', mod_stringg)
            return mod_string

        data_dict = db_customer_check.to_dict()
        name = removing(data_dict.get('first_name', {}).values())
        house_number = removing(data_dict.get('House_number', {}).values())
        villa_Appartment_name = removing(
            data_dict.get('villa_name /Appartment_name', {}).values())
        area_name = removing(data_dict.get('area_name', {}).values())
        road_number = removing(data_dict.get('road_number', {}).values())

        new_order = (
            f"New Order Recived, Number {Entered_Number} and Product {selected_product} with quantity {inputt} {metric}, Customer Name {name} and Address House Number {house_number} ,Area Name {area_name} ,Villa or Appartment Name {villa_Appartment_name}, Road Number {road_number}"
        )
        sent_response = (
            f"Hey {name}, Your Product  {selected_product} with  quantity {inputt} {metric} is Recived! and will be delivered soon to House Number {house_number} ,Area Name {area_name} ,Villa or Appartment Name {villa_Appartment_name}, Road Number {road_number}.  Our Team will get back to you soon, Thanks For Ordering .. Feel Free to Give any Suggestions"
        )
        options_msg = bot.send_message(options_msg.chat.id, sent_response)
        print("new_order:", new_order)
    Add_Subject_Message_Send(new_order, Entered_Number, selected_product,
                             inputt, metric)


# #endless running shuru
keep_alive()
bot.polling()
