# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 18:59:23 2024

@author: neutr
"""

import string
import requests
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import numpy as np
from typing import List, Dict, Set, Tuple
import string


# Download the poem and save it 
# Define the URL of the file
url = "https://openbible.com/textfiles/erv.txt"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Save the content to a local file
    with open('bible_erv.txt', 'wb') as file:
        file.write(response.content)
    print("File saved successfully.")
else:
    print(f"Failed to download file. Status code: {response.status_code}")

if response.status_code == 200:
    bible = response.text
else:
    raise Exception(f"Failed to download file. Status code: {response.status_code}")

def unique_items(items: Set[str]) -> Set[str]:
    return set(items)

# Remove punctuation and convert to lowercase
translator = str.maketrans('', '', string.punctuation)
cleaned_poem = bible.translate(translator).lower()
words = cleaned_poem.split()

# Convert list of words to a set to get unique words
unique_words = unique_items(set(words))
#print(unique_words)
print('\n', 'Number of unique words in the Bible(Eng): ', len(unique_words))

# Define lists of words to exclude
exclude = {
    'saith','every','these','because','down','therefore',
    'give','say','enter','may','let','yet','than','such','upon','unto','psalm','said',
    'came','were','had','also','shalt', 'against','before','even', 'made','went','saying',
    'hath','do','go','come','mer','am','should','was','doth','into','ye','behold',
    '1','2','3','4','5','6','7','8','9','10',
    'jul','rom','one','ben','how','would','too','sir','jul','some','up','where','out','when',
    'is','thy','thee','be','shall','no','as','so','by','will','what','o','all','have','then',
    'from','now','here','if','on','or','an','at','not','are','more','there','well','which',
    'not', 'the', 'a', 'of', 'for', 'thou', 'but', 'and', 'to', 'this','that', 'in','with',
    'i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves'
}

# Function to count words in the text, excluding pronouns and adverbs
def word_count(text: str) -> Counter:
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translator).lower()
    words = cleaned_text.split()
    filtered_words = [word for word in words if word not in exclude]
    return Counter(filtered_words)

# Count words in the poem
word_counts = word_count(bible)

# Get the the number most common words
n=20
most_common_words = dict(word_counts.most_common(n))

colorm='viridis'
print('\nMaking wordcloud')
# Create a word cloud
wordcloud = WordCloud(
    width=800, 
    height=400, 
    background_color='white', 
    colormap=colorm
    ).generate_from_frequencies(most_common_words)
# colormaps:
    # viridis
    # plasma
    # inferno
    # magma
    # cividis
    # Blues
    # Greens
    # Reds
    # Purples
    # coolwarm


# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title(f'Top {n} Most Frequent Words (Excluding meaningless) in the Bible')

# Save the plot as a JPEG file with variable in filename
jpeg_filename = f'Bible_{n}_most_popular_words_wordcloud.jpeg'
plt.savefig(jpeg_filename, format='jpeg')

# Save the plot as a PNG file with variable in filename
png_filename = f'Bible_{n}_most_popular_words_wordcloud.png'
plt.savefig(png_filename, format='png')

# Display the plot
plt.show()

print('Wordcloud is done\n')

print('Making bar chart')
# Separate words and their counts for plotting 
words = list(most_common_words.keys()) 
counts = list(most_common_words.values())

# Apply a colormap to the bar chart 
colors = plt.cm.viridis(np.linspace(0, 1, len(words)))

# Create a bar chart 
plt.figure(figsize=(12, 8)) 
plt.barh(words, counts, color=colors) 
plt.xlabel('Frequency') 
plt.ylabel('Words') 
plt.title(f'Top {n} Most Frequent Words (Excluding useless) in the Bible') 
plt.gca().invert_yaxis() # Invert y-axis to have the most frequent words at the top 

# Save the plot as a JPEG file with variable in filename
jpeg_filename = f'Bible_{n}_most_popular_words_bar.jpeg'
plt.savefig(jpeg_filename, format='jpeg')
# Save the plot as a PNG file with variable in filename
png_filename = f'Bible_{n}_most_popular_words_bar.png'
plt.savefig(png_filename, format='png')
# Display the plot
plt.show()
print('Bar chart is done\n')


print('Making pie chart')
# Function to display count instead of percentage in pie chart 
def absolute_value(val): 
    a = int(val/100.*sum(counts)) 
    return f'{a}'

# Create a pie chart 
plt.figure(figsize=(8, 8)) 
plt.pie(counts, labels=words, autopct=absolute_value, colors=plt.cm.plasma(range(len(words)))) 
plt.title(f'Top {n} Most Frequent Words (Excluding useless) in the Bible') 

# Save the plot as a JPEG file with variable in filename
jpeg_filename = f'Bible_{n}_most_popular_words_pie.jpeg'
plt.savefig(jpeg_filename, format='jpeg')
# Save the plot as a PNG file with variable in filename
png_filename = f'Bible_{n}_most_popular_words_pie.png'
plt.savefig(png_filename, format='png')
# Display the plot
plt.show()
print('Pie chart is done')

# Create a DataFrame for the most common words 
df = pd.DataFrame(most_common_words.items(), columns=['Word', 'Frequency']) 
# Create a table plot 
fig, ax = plt.subplots(figsize=(8, 5)) 
ax.axis('tight') 
ax.axis('off') 
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center') 

# Modify column headers font size and make them bold 
for key, cell in table.get_celld().items(): 
    if key[0] == 0: # Header row 
        cell.set_text_props(fontsize=14, fontweight='bold') 
        
# Add title and adjust layout to move the title up 
plt.title(f"{n} Most Common Words in the Bible", pad=25) 
plt.subplots_adjust(top=0.85) # Adjust top to move title up

# Save the table as an image 
plt.savefig(f"Bible_{n}_most_common_words_table.png", bbox_inches='tight', 
            pad_inches=1, format='png') 
# Save the table as an image 
plt.savefig(f"Bible_{n}_most_common_words_table.jpeg", bbox_inches='tight', 
            pad_inches=1, format='jpeg') 
# Display the table 
plt.show()
print('\nTable is done')

