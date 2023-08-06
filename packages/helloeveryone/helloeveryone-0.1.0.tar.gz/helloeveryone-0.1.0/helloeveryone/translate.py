
from random import choice

from google.cloud import translate


def main():

    # Instantiates a client
    client = translate.Client()

    # The text to translate
    text = u"Hello, everyone"

    # The target language
    target = choice(client.get_languages())

    # Translation
    translation = client.translate(text, target_language=target["language"])

    print(u"Language: '{}'".format(target["name"]))
    print(u"Text: '{}'".format(text))
    print(u"Translation: '{}'".format(translation["translatedText"]))


if __name__ == "__main__":
    main()
