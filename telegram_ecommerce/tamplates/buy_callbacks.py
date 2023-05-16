from telegram import LabeledPrice
##################################
SHIPPING_ADDRESS = range(1)
#################################
from telegram.ext import (
    Filters,
    PreCheckoutQueryHandler,
    MessageHandler,
############################
    ConversationHandler)
###############################

from ..language import get_text
from ..utils.consts import provider_token, currency
from .rating import ask_if_user_want_avaluate_the_product
from ..database.manipulation import (
    add_orders,
    product_has_purchased)


products_data_key = "list_of_products"


def add_pre_checkout_query_to_user_data(context, query):
    context.user_data["last_order"] = query
########################################
def send_a_shipping_message(update, context, product, pattern_identifier):
    chat_id = update.effective_chat.id
    
    # ask user for shipping address
    context.bot.send_message(chat_id=chat_id, text="Please enter your shipping address:")
    
    # wait for user's response
    address_handler = MessageHandler(Filters.text & ~Filters.command, lambda u, c: shipping_address_handler(u, c, product, pattern_identifier))
    context.dispatcher.add_handler(address_handler)
    
    # set timer to remove address_handler after 2 minutes
    context.job_queue.run_once(remove_handler, 120, context=chat_id)
    
    # store the address_handler in context to remove it later
    context.user_data['address_handler'] = address_handler
    
def shipping_address_handler(update, context, product, pattern_identifier):
    chat_id = update.effective_chat.id
    address = update.message.text
    
    # send order confirmation message to user
    message = f"Your order for {product.name} has been placed successfully!\nThe total cost is {product.price}.\nYour order will be shipped to: {address}.\nUse /show_categories or /search to shop more."
    context.bot.send_message(chat_id=chat_id, text=message)
    #ask_if_user_want_avaluate_the_product(update, context, product)
    
    # remove address_handler from dispatcher
    address_handler = context.user_data.get('address_handler')
    if address_handler:
        context.dispatcher.remove_handler(address_handler)
        del context.user_data['address_handler']  # remove it from the context as well

def remove_handler(context, handler):
    context.dispatcher.remove_handler(handler)


# def send_a_shipping_message(update, context, product, pattern_identifier):
#     chat_id = update.effective_chat.id
    
#     # ask user for shipping address
#     context.bot.send_message(chat_id=chat_id, text="Please enter your shipping address:")
    
#     # wait for user's response
#     address_handler = MessageHandler(Filters.text & ~Filters.command, lambda u, c: shipping_address_handler(u, c, product, pattern_identifier))
#     context.dispatcher.add_handler(address_handler)
    
#     # set timer to remove address_handler after 5 minutes
#     context.job_queue.run_once(remove_handler, 120, context=chat_id)
    
# def shipping_address_handler(update, context, product, pattern_identifier):
#     chat_id = update.effective_chat.id
#     address = update.message.text
    
#     # send order confirmation message to user
#     message = f"Your order for {product.name} has been placed successfully!\nThe total cost is {product.price}.\nYour order will be shipped to: {address}."
#     context.bot.send_message(chat_id=chat_id, text=message)
    
#     # remove address_handler from dispatcher
#     context.dispatcher.remove_handler(next(iter(context.dispatcher.handlers)))


#######################################################################################
# def send_a_shipping_message(update, context, product, pattern_identifier):
#     message = f"Your order for {product.name} has been placed successfully! The total cost is {product.price}."
#     context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# def send_a_shipping_message(update, context, product, pattern_identifier):
#     message = f"Your order for {product} has been placed successfully! The total cost is {pattern_identifier}."
#     context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# def send_a_shipping_message(update, context, product, pattern_identifier):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Your order has been placed successfully!")

# def send_a_shipping_message(update, context, product , pattern_identifier):
#     title = product.name
#     description = product.description
#     payload = str(product.product_id)
#     start_parameter = "test-payment"
#     prices = [LabeledPrice("Price", int( 100 * product.price))]


#     context.bot.send_invoice(
#         update.effective_chat.id, 
#         title, 
#         description, 
#         payload, 
#         provider_token, 
#         start_parameter, 
#         currency,
#         prices,
#         need_name = True,
#         need_phone_number = True, 
#         need_email = True, 
#         need_shipping_address = True
#     )


def process_order(query, product, context):
    PROCESS_OK, PROCESS_FAIL = (True, False)
    if query.invoice_payload != str(product.product_id):
        return (PROCESS_FAIL, get_text("information_dont_match", context))
    try:
        add_orders(
            query.id,
            (query.total_amount / 100),
            query.from_user.id,
            product.product_id)
        product_has_purchased(product.product_id)
        return (PROCESS_OK, None) 
    except:
        return (PROCESS_FAIL, get_text("error_in_orders", context))


def pre_checkout_callback(update, context):
    query = update.pre_checkout_query
    add_pre_checkout_query_to_user_data(context, query)
    product = context.user_data[products_data_key]["products"].actual()
    (status, error_message) = process_order(query, product, context)
    if status:
        query.answer(ok=True)
    else:
        query.answer(ok=False, error_message=error_message)


def successful_payment_callback(update, context):
    product = context.user_data[products_data_key]["products"].actual()
    update.message.reply_text(get_text("successful_payment", context))
    ask_if_user_want_avaluate_the_product(update, context, product)


pre_checkout_handler = PreCheckoutQueryHandler(pre_checkout_callback)


successful_payment_handler = MessageHandler(
    Filters.successful_payment, successful_payment_callback)


