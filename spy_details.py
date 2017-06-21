from datetime import datetime

class Spy:
    def __init__(self, name, salutation, age, rating):
        self.name = name
        self.salutation = salutation
        self.age = age
        self.rating = rating
        self.is_online = True
        self.chats = []
        self.current_status_message = None


class ChatMessage:
    def __init__(self, message, sent_by_me):
        self.message = message
        self.time = datetime.now()
        self.sent_by_me = sent_by_me


spy = Spy('bond', 'Mr.', 24, 4.7)

friend_one = Spy('vivek', 'Mr.',27,5)
friend_two = Spy('kawal', 'Ms.',21,5.2)
friend_three = Spy('Nitin', 'Mr.',37,4.3)

friends = [friend_one, friend_two, friend_three]
