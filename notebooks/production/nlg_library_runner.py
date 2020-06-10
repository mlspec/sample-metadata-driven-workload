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

        # print(f"{phrase}\t{return_string}")
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
Children who spend more time outdoors have a lower risk of myopia.
The idea that reading makes you short-sighted has been popular for a couple of hundred years.
Most people think computers will never be able to think.
It is more time-efficient to do several tasks sequentially than attempt to do them simultaneously.
I should stop procrastinating.
I know you think you understood what you thought I said, but I'm not sure you realized that what you heard is not what I meant.
How can video games inspire us to make better applications for e-learning?
No, I'm not afraid of ghosts.
If I could rearrange the alphabet, I would put U and I together.
    """
    bork.generate_sentences(list_of_sentences)