from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request
import datetime, re, os

from goodbooks_config import config
from book_query import BookQuery

app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(config[config_name])
ask = Ask(app, "/")

# Total number of book results to read for a search
TOTAL = 5

# Goodreads API key
gr_api_key = open("goodreads.key","r")
GR_API_KEY = gr_api_key.read()

def _welcome_msg():
    welcome = render_template('welcome')
    opening = render_template('opening_line')
    example = render_template('example')
    return question(welcome + " " + opening) \
            .reprompt("<speak> " + opening + " " + example + " </speak>")

def _help():
    help_text = render_template('help')
    example = render_template('example')
    example_card = render_template('example_for_card')
    opening = render_template('opening_line')
    help_with_ex = help_text + " " + example
    help_with_ex_card = help_text + " " + example_card
    prompt = help_with_ex + " " + opening
    help_card_title = render_template('help_card_title')
    return question("<speak> " + prompt + " </speak>") \
            .simple_card(title=help_card_title,content=help_with_ex_card)

def _get_first_book_entry(book_list):
    '''
        Render the first book from the book list. And persist the remaining list in the session
    '''
    if len(book_list) > 0:
        # persist top entry in the book list and rest of the list
        current_book = book_list.pop(0)
        session.attributes['current_book'] = current_book
        session.attributes['book_list'] = book_list

        msg = 'book_result'
    else:
        if session.attributes.get('book_list') == None:
            # If first time this function is called (by checking if book_list session attributes is set)
            msg = 'no_book_result'
        else:
            msg = 'no_more_book_result'

    return msg


# ***************************** Alexa functions ********************************

def _book_output_data(msg):
    '''
        function to generate book data for alexa voice and card.
    '''
    if msg == 'book_result':
        book_prompt = render_template(msg,book=session.attributes.get('current_book'))
        next_prompt = render_template('next_book_result')
        book_card_title = render_template('book_card_title',book=session.attributes.get('current_book'))
        return question(book_prompt).simple_card(title=book_card_title,content=book_prompt).reprompt(next_prompt)
    else: # if no result
        prompt = render_template(msg) + " " + render_template('opening_line')
        return question(prompt)

@ask.launch
def start_app():
    return _welcome_msg()

@ask.intent("GetFirstBookIntent",convert={'book_title': str,'book_author': str})
def get_book_list(book_title,book_author):

    bq = None
    # Try to query by book title first
    if book_title != None:
        bq = BookQuery(GR_API_KEY,book_title)
    # If book title is missing, go for author
    elif book_author != None:
        bq = BookQuery(GR_API_KEY,book_author)

    if bq == None or bq.books == None or len(bq.books) == 0:
        msg = render_template('missing_books')
        return statement(msg)

    book_list = []
    for book_id,title,author_id,author_name,rating,published in bq.get_book():
        if book_author == None or book_author == "":
            # If no author is specified, add the book to the list by default
            book_list.append({  "book_id":book_id,
                                "title": title,
                                "author_id": author_id,
                                "author_name": author_name,
                                "rating": rating,
                                "published": published})
        elif book_author.lower() == author_name.lower():
            # If author is specified only add books of that author
            book_list.append({  "book_id":book_id,
                                "title": title,
                                "author_id": author_id,
                                "author_name": author_name,
                                "rating": rating,
                                "published": published})

        if len(book_list) == TOTAL:
            break

    msg = _get_first_book_entry(book_list)

    return _book_output_data(msg)


@ask.intent("GetNextBookIntent")
def next_title():
    book_list = []
    try:
        book_list = session.attributes['book_list']
    except KeyError:
        return _help()

    msg = _get_first_book_entry(book_list)

    return _book_output_data(msg)


@ask.intent('AMAZON.HelpIntent')
def help():
    return _help()

@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = render_template('bye')
    return statement(bye_text)

@ask.intent('AMAZON.CancelIntent')
def cancel():
    bye_text = render_template('bye')
    return statement(bye_text)

@ask.session_ended
def session_ended():
    return statement('')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
