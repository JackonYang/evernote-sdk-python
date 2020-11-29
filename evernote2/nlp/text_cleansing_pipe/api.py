# from .algorithms.non_ascii import clean_non_ascii
from .algorithms.html_cleaner import clean_text_for_hash

TEXT_MAX_LEN = None


def clean_long_html_for_nlp(text):
    if not text:
        return ''

    if TEXT_MAX_LEN is not None:
        text = text[TEXT_MAX_LEN]

    # feed to pipeline steps one by one
    # add more steps if you want
    # text = clean_non_ascii(text)
    text = clean_text_for_hash(text, keep_new_line=False)

    return text


# def clean_long_html_for_display(text):
#     if not text:
#         return ''

#     if settings.FAST_MODE:
#         return text

#     text = tags_cleaner.clean(text)

#     # text_bak = text
#     text = split_joined_words(text)
#     # if text != text_bak:
#     #     import csv
#     #     with open('touching_words_compare.csv', 'a') as csvfile:
#     #         csv_writer = csv.writer(csvfile)

#     #         for s in re.split(r'[.<>!:]+', text_bak):
#     #             s_cleaned = split_joined_words(s)
#     #             if s != s_cleaned:
#     #                 csv_writer.writerow([s.encode('utf8'), s_cleaned.encode('utf8')])

#     non_html_text = text

#     text = pretty_html(text)

#     if '\n' not in text:
#         non_html_text = remove_space(newline_ptn.sub('<br/>', non_html_text.strip()))
#         text = pretty_html(non_html_text)

#     text = remove_extra_br(text)

#     return text


if __name__ == '__main__':
    res = clean_long_html_for_nlp('asdfasfkasjf')
    print(res)
