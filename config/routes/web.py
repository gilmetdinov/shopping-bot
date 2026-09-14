from enum import Enum


class WebRoutes(Enum):
    ping = '/'
    test = '/test'
    hook = '/api/telegram/webhook'
    sendMessage = '/api/send-message'
    sendMessageMass = '/api/send-message-mass'
    sendNotification = '/api/send-notification'
    sendNotificationMass = '/api/send-notification-mass'
