import pandas as pd
from urlextract import URLExtract
from collections import Counter
extractor = URLExtract()
import emoji
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    num_messages = df.shape[0]

    words = []
    links = []
    emojis = []
    for message in df['messages']:
        words.extend(message.split())
        links.extend(extractor.find_urls(message))
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    image_count = df['messages'].str.count('image omitted').sum()
    video_count = df['messages'].str.count('video omitted').sum()
    audio_count = df['messages'].str.count('audio omitted').sum()
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return num_messages, words, image_count, video_count, audio_count, len(links), emoji_df

def create_wordcloud(selected_user, df):

    df = df[~df['messages'].str.contains('image omitted')]
    df = df[~df['messages'].str.contains('audio omitted')]
    df = df[~df['messages'].str.contains('video omitted')]

    df = df[df['users'] != 'group notification']

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=" "))

    return df_wc

def user_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]



'''
    if selected_user == 'Overall':
        # fetch number of messages
        num_messages = df.shape[0]

        words = []
        for message in df['messages']:
            words.extend(message.split())

        return num_messages, words

    else:
        new_df = df[df['users'] == selected_user]
        num_messages = new_df.shape[0]
        words = []
        for message in new_df['messages']:
            words.extend(message.split())

        return num_messages, words
'''