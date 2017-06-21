from termcolor import colored
from spy_details import spy, Spy, ChatMessage, friends
from steganography.steganography import Steganography
import re

print "Hello.\n"
total_words = 0
total_images = 0

STATUS_MESSAGES = ['My name is Bond, James Bond', 'Shaken, not stirred.', 'Keeping the British end up, Sir']

question = "Do you want to continue as " + spy.salutation + " " + spy.name + " (Y/N)? "
existing = raw_input(question)


# function which adds a status to your spy
def add_status():
    updated_status_message = None

    if spy.current_status_message != None:

        print 'Your current status message is %s \n' % (spy.current_status_message)
    else:
        print 'You don\'t have any status message currently \n'

    default = raw_input("Do you want to select from the older status (y/n)? ")

    if default.upper() == "N":
        new_status_message = raw_input("What status message do you want to set? ")

        if len(new_status_message) > 0:
            STATUS_MESSAGES.append(new_status_message)
            updated_status_message = new_status_message

    elif default.upper() == 'Y':

        item_position = 1

        for message in STATUS_MESSAGES:
            print '%d. %s' % (item_position, message)
            item_position = item_position + 1

        message_selection = int(raw_input("\nChoose from the above messages "))

        if len(STATUS_MESSAGES) >= message_selection:
            updated_status_message = STATUS_MESSAGES[message_selection - 1]

    else:
        print 'The option you chose is not valid! Press either y or n.'

    if updated_status_message:
        print 'Your updated status message is: %s' % (updated_status_message)
    else:
        print 'You don\'t have a status update'

    return updated_status_message


# function adds your friend
def add_friend():
    new_friend = Spy('', '', 0, 0.0)

    new_friend.name = raw_input("Please add your friend's name: ")
    new_friend.salutation = raw_input("Are they Mr. or Ms.?: ")

    new_friend.name = new_friend.salutation + " " + new_friend.name

    new_friend.age = raw_input("Age?")
    new_friend.age = int(new_friend.age)

    new_friend.rating = raw_input("Spy rating?")
    new_friend.rating = float(new_friend.rating)

    if len(new_friend.name) > 0 and new_friend.age > 12 and new_friend.rating >= spy.rating and new_friend.age < 50:
        friends.append(new_friend)
        print 'Friend Added!'
    else:
        print 'Sorry! Invalid entry. We can\'t add spy with the details you provided'

    return len(friends)


# function shows your friend list.
def select_a_friend():
    item_number = 0

    for friend in friends:
        print '%d. %s %s aged %d with rating %.2f is online' % (item_number + 1,
                                                                friend.salutation,
                                                                friend.name,
                                                                friend.age,
                                                                friend.rating)
        item_number = item_number + 1

    friend_choice = raw_input("Choose from your friends")

    friend_choice_position = int(friend_choice) - 1

    return friend_choice_position


# function that sends the image after encrypting text into it.
def send_message():
    friend_choice = select_a_friend()

    original_image = raw_input("What is the name of the image?")
    output_path = "output.jpg"
    text = raw_input("What do you want to say? ")
    Steganography.encode(original_image, output_path, text)

    new_chat = ChatMessage(text, True)

    friends[friend_choice].chats.append(new_chat)

    print "Your secret message image is ready!"


# function which reads the massage from a image file.
def read_message():
    global total_words
    global total_images

    total_images += 1
    sender = select_a_friend()

    output_path = raw_input("What is the name of the file?")

    secret_text = Steganography.decode(output_path)

    new_chat = ChatMessage(secret_text, False)

    if secret_text=="SOS" or secret_text == "SAVE ME":
        print colored('\nReinforcement will soon be their\n', 'red')

    if len(secret_text) > 0:
       wordList = re.sub("[^\w]", " ", secret_text).split()
       if len(wordList) > 100:
           del friends[sender]
       else:
        total_words += len(wordList)
        friends[sender].chats.append(new_chat)
        print "Your secret message has been saved!"
    else:
       print "Image is not having any secret massage"


# funtion reads the chat history between you and your friends.
def read_chat_history():
    read_for = select_a_friend()

    for chat in friends[read_for].chats:
        if chat.sent_by_me:
            print colored('[%s]'% (chat.time.strftime("%d %B %Y")),'blue')
            print colored('You said: ' , 'red')
            print (chat.message+'\n')
        else:
           print colored('[%s]' % (chat.time.strftime("%d %B %Y")), 'blue')
           print colored(friends[read_for].name+' said :', 'red')
           print (chat.message+'\n')


# function which shhows the main menu.
def start_chat(spy):
    spy.name = spy.salutation + " " + spy.name

    if spy.age > 12 and spy.age < 50:

        print "Authentication complete. Welcome " + spy.name + ", age: " \
              + str(spy.age) + " and rating of: " + str(spy.rating) + " Proud to have you onboard"

        show_menu = True

        while show_menu:
            menu_choices = "What do you want to do? \n " \
                           "1. Add a status update \n " \
                           "2. Add a friend \n " \
                           "3. Send a secret message \n " \
                           "4. Read a secret message \n " \
                           "5. Read Chats from a user \n" \
                           " 6. Close Application \n"

            menu_choice = raw_input(menu_choices)

            if len(menu_choice) > 0:
                menu_choice = int(menu_choice)

                if menu_choice == 1:
                    spy.current_status_message = add_status()
                elif menu_choice == 2:
                    number_of_friends = add_friend()
                    print 'You have %d friends' % (number_of_friends)
                elif menu_choice == 3:
                    send_message()
                elif menu_choice == 4:
                    read_message()
                elif menu_choice == 5:
                    read_chat_history()
                else:
                    print ' Average number of words spoken %d ' % (total_words/total_images)
                    show_menu = False
    else:
        print 'Sorry you are not of the correct age to be a spy'


if existing.upper() == "Y":
    start_chat(spy)
else:

    spy = Spy('', '', 0, 0.0)

    spy.name = raw_input("Welcome to spy chat, you must tell me your spy name first: ")

    if len(spy.name) > 0:
        spy.salutation = raw_input("Should I call you Mr. or Ms.?: ")

        spy.age = raw_input("What is your age?")
        spy.age = int(spy.age)

        if spy.age < 12 or spy.age > 50:
            print 'Sorry! Not a valid age to become a spy'

        else:
            spy.rating = raw_input("What is your spy rating?")
            spy.rating = float(spy.rating)

            if spy.rating > 4.5:
                print 'Great ace!'
            elif spy.rating > 3.5 and spy.rating <= 4.5:
                print 'You are one of the good ones.'
            elif spy.rating >= 2.5 and spy.rating <= 3.5:
                print 'You can always do better'
            else:
                print 'We can always use somebody to help in the office.'

            start_chat(spy)
    else:
        print 'Please add a valid spy name'
