show_categories = ConversationHandler(
    entry_points = [show_categories_command],
    states = {
        ASK_FOR_CATEGORY_NAME : [
            MessageHandler(
                Filters.text, 
                ask_for_category_name)
            ],
        GET_LIST_OF_PRODUCTS : [
            MessageHandler(
                Filters.text, 
                get_list_of_products)
            ],
        SHOW_LIST_OF_PRODUCTS : [
            MessageHandler(
                Filters.text, 
                show_list_of_products
                ),
            CallbackQueryHandler(
                catch_next, 
                pattern = pattern_identifier +
                PATTERN_TO_CATCH_THE_NEXT_PRODUCT),
            CallbackQueryHandler(
                catch_previus, 
                pattern = pattern_identifier +
                PATTERN_TO_CATCH_THE_PREVIUS_PRODUCT),
            CallbackQueryHandler(
                catch_details,
                pattern = pattern_identifier +
                PATTERN_TO_CATCH_THE_VIEW_DETAILS)
            ],
        BUY_PROCESS : [
            CallbackQueryHandler(
                catch_previus, 
                pattern = pattern_identifier +
                PATTERN_TO_CATCH_THE_PREVIUS_PRODUCT),
            CallbackQueryHandler(
                send_a_shipping_message_callback, 
                pattern = pattern_identifier + 
                PATTERN_TO_CATCH_THE_BUY_BUTTON)
            ]
        },
    fallbacks = [MessageHandler(Filters.all, cancel_show_categories)]
    )
