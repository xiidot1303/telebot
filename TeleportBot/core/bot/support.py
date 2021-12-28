from telegram.ext import ConversationHandler, MessageHandler, CallbackQueryHandler, Filters as TelegramFilters
from telegram import ParseMode

from core.services import users, settings
from core.resources import strings, keyboards, images, utils
from .utils import Filters, Navigation
from config import Config
from . import about, account, faq, news, referral

from datetime import datetime
import pytz

SUPPORT = range(1)


def start(update, context):
    user_id = update.message.from_user.id
    if 'user' not in context.user_data:
        context.user_data['user'] = users.user_exists(user_id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.message.reply_text(blocked_message)
        return ConversationHandler.END
    context.user_data['has_action'] = True
    language = context.user_data['user'].get('language')
    bot_settings = settings.get_settings()
    support_message = bot_settings.get('support_' + language)
    if not support_message:
        support_message = strings.get_string('support.welcome', language).format(name=context.user_data['user'].get('name'))
    support_message = utils.replace_new_line(support_message)
    support_keyboard = keyboards.get_keyboard('support.cancel', language)
    image = None
    if bot_settings.get('support_image_' + language):
        try:
            image = open(bot_settings.get('support_image_' + language), 'rb')
        except FileNotFoundError:
            pass
    if not image:
        image = images.get_support_image(language)
    if image:
        chat_id = update.message.chat_id
        message = context.bot.send_photo(chat_id=chat_id, photo=image, caption=support_message,
                                         reply_markup=support_keyboard, parse_mode=ParseMode.HTML)
    else:
        message = update.message.reply_text(text=support_message, reply_markup=support_keyboard, parse_mode=ParseMode.HTML)
    context.user_data['support_message'] = message
    return SUPPORT


def support(update, context):
    language = context.user_data['user'].get('language')
    if strings.get_string('cancel', language) in update.message.text:
        canceled_message = strings.get_string('support.canceled', language)
        update.message.reply_text(canceled_message)
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.user_data['support_message'].message_id)
        Navigation.to_main_menu(update, language, user_name=context.user_data['user'].get('name'))
        del context.user_data['has_action']
        return ConversationHandler.END
    elif update.message:
        user_id = update.message.from_user.id
        question_text = update.message.text
        bot_info = context.bot.get_me()
        timezone = pytz.timezone('Asia/Tashkent')
        now_date = datetime.now(tz=timezone).strftime('%d %B %Y %H:%M:%S')
        support_message = strings.get_string('support.question.template', 'ru').format(bot_id=bot_info.id,
                                                                                       bot_name=bot_info.first_name,
                                                                                       user_id=user_id,
                                                                                       user_name=context.user_data[
                                                                                           'user'].get('name'),
                                                                                       date=now_date,
                                                                                       question=question_text)
        support_keyboard = keyboards.get_support_keyboard(link=(Config.APP_URL + '/users/' + str(user_id) + '/edit'))
        context.bot.send_message(chat_id=Config.TELEGRAM_SUPPORT_GROUP, text=support_message, parse_mode=ParseMode.HTML,
                                 reply_markup=support_keyboard)
        message = context.user_data['support_message']
        context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
        success_message = strings.get_string('support.success', language)
        update.message.reply_text(text=success_message)
        Navigation.to_main_menu(update, language, context=context)
        del context.user_data['has_action']
        return ConversationHandler.END
    else:
        return SUPPORT


support_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.SupportFilter, start)],
    states={
        SUPPORT: [MessageHandler(TelegramFilters.text, support)]
    },
    fallbacks=[
        account.account_handler,
        referral.referral_handler,
        faq.faq_handler,
        about.about_handler,
        news.news_handler
    ]
)
