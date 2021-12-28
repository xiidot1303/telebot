from core.resources import strings, keyboards, images
from telegram.ext import BaseFilter, MessageHandler
from core.services import users
from telegram.error import BadRequest
import threading


class Navigation:
    @staticmethod
    def to_main_menu(update, language, message_text=None, user_name=None, context=None, welcome=False):
        if message_text:
            menu_message = message_text
        else:
            if welcome:
                menu_message = strings.get_string('start.welcome', language).format(username=user_name)
            else:
                menu_message = strings.get_string('menu.welcome', language)
        menu_keyboard = keyboards.get_keyboard('menu', language)
        if update.message:
            chat_id = update.message.chat_id
        else:
            chat_id = update.callback_query.message.chat_id
        if welcome:
            image = images.get_welcome_image(language)
            if image:
                context.bot.send_photo(chat_id=chat_id, photo=image, caption=menu_message, reply_markup=menu_keyboard)
            else:
                context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=menu_message,
                                         reply_markup=menu_keyboard)
        else:
            if update.message:
                update.message.reply_text(menu_message, reply_markup=menu_keyboard)
            else:
                context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=menu_message,
                                         reply_markup=menu_keyboard)

    @staticmethod
    def to_account(update, context, new_message=False):
        if update.message:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        if 'user' not in context.user_data:
            context.user_data['user'] = users.user_exists(user_id)
        user = context.user_data['user']
        account_message = strings.get_user_info(user)
        account_keyboard = keyboards.get_account_keyboard(user)
        image = images.get_account_image(context.user_data['user'].get('user_role'),
                                         context.user_data['user'].get('language'))
        if update.message:
            if image:
                message = context.bot.send_photo(chat_id=user_id, photo=image, caption=account_message,
                                                 reply_markup=account_keyboard)
            else:
                message = update.message.reply_text(text=account_message, reply_markup=account_keyboard)
        elif update.callback_query:
            if new_message:
                if image:
                    message = context.bot.send_photo(chat_id=user_id, photo=image, caption=account_message,
                                                     reply_markup=account_keyboard)
                else:
                    message = context.bot.send_message(chat_id=user_id, text=account_message, reply_markup=account_keyboard)
            else:
                if image:
                    context.bot.delete_message(chat_id=user_id, message_id=update.callback_query.message.message_id)
                    message = context.bot.send_photo(chat_id=user_id, photo=image, caption=account_message,
                                                     reply_markup=account_keyboard)
                else:
                    update.callback_query.edit_message_text(text=account_message, reply_markup=account_keyboard)
                    return
        else:
            return
        if 'account_message_id' in context.user_data:
            try:
                context.bot.delete_message(chat_id=user_id, message_id=context.user_data['account_message_id'])
            except BadRequest:
                pass
        context.user_data['account_message_id'] = message.message_id


class Filters:

    class AccountFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.cabinet', 'ru') in message.text or
                                     strings.get_string('menu.cabinet', 'uz') in message.text or
                                     strings.get_string('menu.cabinet', 'latuz') in message.text)

    class ReferralFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.referral', 'ru') in message.text or
                                     strings.get_string('menu.referral', 'uz') in message.text or
                                     strings.get_string('menu.referral', 'latuz') in message.text)

    class FaqFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.faq', 'ru') in message.text or
                                     strings.get_string('menu.faq', 'uz') in message.text or
                                     strings.get_string('menu.faq', 'latuz') in message.text)

    class AboutFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.about', 'ru') in message.text or
                                     strings.get_string('menu.about', 'uz') in message.text or
                                     strings.get_string('menu.about', 'latuz') in message.text)

    class PartnersFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.partners', 'ru') in message.text or
                                     strings.get_string('menu.partners', 'uz') in message.text or
                                     strings.get_string('menu.partners', 'latuz') in message.text)

    class NewsFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.news', 'ru') in message.text or
                                     strings.get_string('menu.news', 'uz') in message.text or
                                     strings.get_string('menu.news', 'latuz') in message.text)

    class SupportFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.support', 'ru') in message.text or
                                     strings.get_string('menu.support', 'uz') in message.text or
                                     strings.get_string('menu.support', 'latuz') in message.text)


class Notifications:

    class NotificationThread:

        def __init__(self, bot, notifiable_users, string_resource):
            thread = threading.Thread(target=self.run, kwargs={'bot': bot, 'notifiable_users': notifiable_users,
                                                               'string_resource': string_resource})
            thread.daemon = True
            thread.start()

        def run(self, **kwargs):
            bot = kwargs.get('bot')
            notifiable_users = kwargs.get('notifiable_users')
            string_resource = kwargs.get('string_resource')
            for user in notifiable_users:
                message = strings.get_string(string_resource, user.get('language'))
                keyboard = keyboards.get_keyboard('notifications.close', user.get('language'))
                try:
                    bot.send_message(chat_id=user.get('id'), text=message, reply_markup=keyboard)
                except BadRequest:
                    continue

    @staticmethod
    def notify_users_new_item(bot, notifiable_users, string_resource):
        Notifications.NotificationThread(bot, notifiable_users, string_resource)
