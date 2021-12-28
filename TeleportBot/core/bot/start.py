from config import Config
from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from core.resources import strings, keyboards
from core.services import users
from .utils import Navigation

LANGUAGES, SUBSCRIPTION = 1, 2


def referral_start(update, context):
    user = users.user_exists(update.message.from_user.id)
    if user:
        if user.get('is_blocked'):
            blocked_message = strings.get_string('blocked', user.get('language'))
            update.message.reply_text(blocked_message)
            return ConversationHandler.END
        Navigation.to_main_menu(update, user.get('language'), user_name=user.get('name'), welcome=True, context=context)
        help_message = strings.get_string('start.help', user.get('language'))
        update.message.reply_text(help_message)
        return ConversationHandler.END
    if context.args:
        context.user_data['referral_from_id'] = context.args[0]
    languages_message = strings.get_string('start.languages')
    keyboard = keyboards.get_keyboard('start.languages')

    update.message.reply_text(languages_message, reply_markup=keyboard)

    return LANGUAGES


def languages(update: Update, context):

    def error():
        languages_message = strings.get_string('start.languages')
        keyboard = keyboards.get_keyboard('start.languages')
        update.message.reply_text(languages_message, reply_markup=keyboard)

    text = update.message.text
    if strings.get_string('languages.ru') in text:
        language = 'ru'
    elif strings.get_string('languages.uz') in text:
        language = 'uz'
    elif strings.get_string('languages.latuz') in text:
        language = 'latuz'
    else:
        error()
        return LANGUAGES
    user = update.message.from_user
    user_name = _get_user_name(user)
    users.create_user(user.id, user_name, user.username, language,
                      referral_from_id=context.user_data.get('referral_from_id', None))
    chat_id = update.effective_message.chat_id
    check = check_subscription(context, chat_id)
    if check == True:
        Navigation.to_main_menu(update, language, user_name=user_name, welcome=True, context=context)
        return ConversationHandler.END
    else:
        languages_message = strings.get_string('subscription', language)
        keyboard = keyboards.get_keyboard('subscription_btn', language)
        update.message.reply_text(languages_message, reply_markup=keyboard)
        return SUBSCRIPTION
    # help_message = strings.get_string('start.help', language)
    # update.message.reply_text(help_message)


def subscription(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    query = update.callback_query
    check = check_subscription(context, chat_id)
    if query.data == "confirm":
        if check == False:
            user = users.user_exists(query.from_user.id)
            language = user.get('language')
            error_msg = strings.get_string('subscription_error', language)
            context.bot.send_message(chat_id=chat_id, text=error_msg)
            return SUBSCRIPTION
        else:
            query.edit_message_text(
                text=update.effective_message.text,
                parse_mode="Markdown"
            )
    user = users.user_exists(chat_id)
    Navigation.to_main_menu(update, user.get('language'), user_name=user.get('name'), welcome=True, context=context)
    return ConversationHandler.END


def check_subscription(context: CallbackContext, chat_id):
    chat_member = context.bot.get_chat_member(chat_id=Config.TELEGRAM_CHANNEL_USERNAME, user_id=chat_id)
    if chat_member.status == "left" or chat_member.status == "kicked":
        return False
    else:
        return True


def _get_user_name(user):
    user_name = user.first_name
    if user.last_name:
        user_name += (" " + user.last_name)
    return user_name


def cancel():
    pass


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', referral_start, pass_args=True)],
    states={
        LANGUAGES: [MessageHandler(Filters.text, languages)],
        SUBSCRIPTION: [CallbackQueryHandler(callback=subscription, pass_chat_data=True)]
    },
    fallbacks=[MessageHandler(Filters.text, '')]
)
