import sys
import time
from random import randint, choice, random
from IPython.display import HTML, display
import tabulate
# table = [["Sun",696000,1989100000],
#          ["Earth",6371,5973.6],
#          ["Moon",1737,73.5],
#          ["Mars",3390,641.85]]

class bork:
    def __init__(self):
        self.bork = "b0rk"

    @staticmethod
    def generate_sentences(phrases: str):
        bork_phrase = "b0rk"
        punctuation_end = ['.', '?', '!', '‽', ]
        punctuation_middle = ['...', ',', ' - ']
        all_sentences = []
        
        phrases = "".join([s for s in phrases.splitlines(True) if s.strip()])

        for phrase in phrases.split('\n'):
            num_of_words = len(phrase.split())

            if num_of_words == 0:
                continue

            return_string = ""

            num_of_borks = randint(1, num_of_words * 2)

            for i in range(num_of_borks):
                j = randint(1,10)
                if i == 0:
                    return_string = f"{bork_phrase.capitalize()} "
                else:
                    return_string += " "
                
                if j < 2:
                    c = choice(punctuation_middle + punctuation_end)
                    if c in punctuation_end: 
                        return_string += choice(punctuation_end)
                        return_string += " " + str.capitalize(bork_phrase)
                elif j < 5:
                    return_string += choice(punctuation_middle)
                    return_string += " " + str.capitalize(bork_phrase)
                else:
                    return_string += bork_phrase

            
            return_string += choice(punctuation_end)

            all_sentences.append([phrase, return_string])

        display(HTML(tabulate.tabulate(all_sentences, tablefmt='html', stralign="left", headers=['Sentence', 'Generated Text'])))

    @staticmethod
    def display_test_data():
        list_of_sentences = """
To whose house are you going?
The people marched for justice.
These questions are easy to answer.
Brad came to dinner with us.
He loves fish tacos.
In the end, we all felt like we ate too much.
We all agreed; it was a magnificent evening.
I hope that, when I've built up my savings, I'll be able to travel to Mexico.
Did you know that, along with gorgeous architecture, it's home to the largest tamale?
Wouldn't it be lovely to enjoy a week soaking up the culture?
Oh, how I'd love to go!
Of all the places to travel, Mexico is at the top of my list.
Would you like to travel with me?
Isn't language learning fun?
There is so much to understand.
I love learning!
Sentences come in many shapes and sizes.
Nothing beats a complete sentence.
Once you know all the elements, it's not difficult to pull together a sentence.
We had a three-course meal.
Brad came to dinner with us.
He loves fish tacos.
In the end, we all felt like we ate too much.
We all agreed; it was a magnificent evening.
I hope that, when I've built up my savings, I'll be able to travel to Mexico.
Did you know that, along with gorgeous architecture, it's home to the largest tamale?
Wouldn't it be lovely to enjoy a week soaking up the culture?
Oh, how I'd love to go!
Of all the places to travel, Mexico is at the top of my list.
Would you like to travel with me?
Isn't language learning fun?
There is so much to understand.
I love learning!
Sentences come in many shapes and sizes.
Nothing beats a complete sentence.
Once you know all the elements, it's not difficult to pull together a sentence.
"""
        bork.generate_sentences(list_of_sentences)

    @staticmethod
    def load_data(test_data, inferSchema):
        pass

    @staticmethod
    def transform(*val):
        accuracy = random() * 30/100
        top = 0.90
        while accuracy < top:
            sys.stdout.write("Accuracy... ".center(30))
            sign = 1 if (randint(0,10) > 2) else -1
            diff = top - accuracy
            diff = 10 if (diff < 10) else diff
            step = sign * diff * random() / 100
            accuracy += step
            sys.stdout.write("{:>6}\n".format(round(accuracy,6)))
            sys.stdout.flush()
            time.sleep(0.1)

    @staticmethod
    def display_auc():
        display(HTML('<img src="aih727ba.bmp" />'))


if __name__ == "__main__":

    list_of_sentences = """
    My mom drove me to school fifteen minutes late on Tuesday.
    The girl wore her hair in two braids, tied with two blue bows.
    The mouse was so hungry he ran across the kitchen floor without even looking for humans.
    The tape got stuck on my lips so I couldn't talk anymore.
    The door slammed down on my hand and I screamed like a little baby.
    My shoes are blue with yellow stripes and green stars on the front.
    The mailbox was bent and broken and looked like someone had knocked it over on purpose.
    I was so thirsty I couldn't wait to get a drink of water.
    I found a gold coin on the playground after school today.
    The chocolate chip cookies smelled so good that I ate one without asking.
    My bandaid wasn't sticky any more so it fell off on the way to school.
    He had a sore throat so I gave him my bottle of water and told him to keep it.
    The church was white and brown and looked very old.
    I was so scared to go to a monster movie but my dad said he would sit with me so we went last night.
    Your mom is so nice she gave me a ride home today.
    I fell in the mud when I was walking home from school today.
    This dinner is so delicious I can't stop eating.
    The school principal was so mean that all the children were scared of him.
    I went to the dentist the other day and he let me pick a prize out of the prize box.
    The box was small and wrapped in paper with tiny silver and red glitter dots.
    My dad is so funny that he told us jokes all night long and we never fell asleep.
    The camping trip was so awesome that I didn't want to come home.
    Are you going to have a blue birthday cake for your next birthday?
    How did you know that I was going to have a peanut butter sandwich for lunch?
    That boy is so mean that he doesn't care if a door slams in your face or if he cuts in line.
    The moms and dads all sat around drinking coffee and eating donuts.
    My mom made a milkshake with frozen bananas and chocolate sauce.
    My pen broke and leaked blue ink all over my new dress.
    I got my haircut today and they did it way too short.
    My pet turtle, Jim, got out of his cage and I could not find him anywhere.
    I would like to go to the library.
    Soon, I'll tell you some good news.
    The man and the woman fell in love.
    I would like to order a cheese omelette.
    """
    bork.generate_sentences(list_of_sentences)