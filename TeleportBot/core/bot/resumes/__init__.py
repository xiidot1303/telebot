from . import create
from . import edit
from . import vacations
from core.bot import about, account, faq, news, support, referral, start
from core.bot.utils import Navigation, Filters as CustomFilters

from telegram.ext import CallbackQueryHandler, MessageHandler, Filters, ConversationHandler, PreCheckoutQueryHandler


def main_menu_handler(update, context):
    if CustomFilters.AboutFilter().filter(update.message):
        about.about(update, context)
    elif CustomFilters.FaqFilter().filter(update.message):
        faq.faq(update, context)
    elif CustomFilters.ReferralFilter().filter(update.message):
        referral.start(update, context)
    elif CustomFilters.AccountFilter().filter(update.message):
        account.start(update, context)
        if 'resume' in context.user_data:
            del context.user_data['resume']
        return ConversationHandler.END
    elif CustomFilters.SupportFilter().filter(update.message):
        support.support_conversation.handle_update(update, context.dispatcher, support.support_conversation.check_update(update), context)
        if 'resume' in context.user_data:
            del context.user_data['resume']
        return ConversationHandler.END
    elif CustomFilters.NewsFilter().filter(update.message):
        news.news(update, context)
    elif '/start' in update.message.text:
        start.referral_start(update, context)
        if 'resume' in context.user_data:
            del context.user_data['resume']
        return ConversationHandler.END
    else:
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)


create_resume_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(create.create, pattern='resumes:create')],
    states={
        create.TITLE: [MessageHandler(Filters.text, create.resume_title)],
        create.DESCRIPTION: [MessageHandler(Filters.text, create.resume_description)],
        create.CONTACTS: [MessageHandler(Filters.text, create.resume_contacts)],
        create.REGION: [CallbackQueryHandler(create.from_location_to_contacts, pattern='region:back'),
                        CallbackQueryHandler(create.resume_region), MessageHandler(Filters.text, main_menu_handler)],
        create.CITY: [CallbackQueryHandler(create.resume_city),
                      MessageHandler(Filters.text, main_menu_handler)],
        create.CATEGORIES: [CallbackQueryHandler(create.from_categories_to_location, pattern='category:to_location'),
                            CallbackQueryHandler(create.resume_categories),
                            MessageHandler(Filters.text, main_menu_handler)],
        create.TARIFFS: [CallbackQueryHandler(create.payments.tariffs), MessageHandler(Filters.text, main_menu_handler)],
        create.PROVIDER: [CallbackQueryHandler(create.payments.providers), MessageHandler(Filters.text, main_menu_handler)],
        create.PRE_CHECKOUT: [PreCheckoutQueryHandler(create.payments.pre_checkout_callback),
                              MessageHandler(Filters.text, create.payments.pre_checkout_callback)],
        create.HISTORY: [CallbackQueryHandler(create.payments.history_handler), MessageHandler(Filters.text, main_menu_handler)]
    },
    fallbacks=[
        account.account_handler,
        referral.referral_handler,
        faq.faq_handler,
        about.about_handler,
        support.support_conversation,
        news.news_handler
    ]
)
action_resume_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit.resume, pattern=r'^resumes:\d+$')],
    states={
        edit.RESUME_ACTION: [CallbackQueryHandler(edit.resume_action), MessageHandler(Filters.text, main_menu_handler)],
        edit.EDIT_ACTION: [CallbackQueryHandler(edit.edit_action), MessageHandler(Filters.text, main_menu_handler)],
        edit.UPDATE_RESUME: [MessageHandler(Filters.text, edit.update_resume)]
    },
    fallbacks=[
        account.account_handler,
        referral.referral_handler,
        faq.faq_handler,
        about.about_handler,
        support.support_conversation,
        news.news_handler
    ]
)
resume_back_handler = CallbackQueryHandler(Navigation.to_account, pattern='resumes:back')

resume_vacations_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(vacations.resumes_list, pattern='account:vacations')],
    states={
        vacations.LIST: [CallbackQueryHandler(vacations.vacations_for_resume), MessageHandler(Filters.text, main_menu_handler)],
        vacations.VACATIONS: [CallbackQueryHandler(vacations.paginated_vacations), MessageHandler(Filters.text, main_menu_handler)]
    },
    fallbacks=[
        account.account_handler,
        referral.referral_handler,
        faq.faq_handler,
        about.about_handler,
        support.support_conversation,
        news.news_handler
    ]
)
