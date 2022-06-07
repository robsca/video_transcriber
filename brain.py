from transformers import pipeline
from bs4 import BeautifulSoup
import requests
import pandas as pd
import plotly.express as px

def summarizer_from_url(URL):
    summarizer = pipeline("summarization")
    r = requests.get(URL)

    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all(['h1', 'p'])
    text = [result.text for result in results]
    ARTICLE = ' '.join(text)

    max_chunk = 500

    ARTICLE = ARTICLE.replace('.', '.<eos>')
    ARTICLE = ARTICLE.replace('?', '?<eos>')
    ARTICLE = ARTICLE.replace('!', '!<eos>')

    sentences = ARTICLE.split('<eos>')
    current_chunk = 0 
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            print(current_chunk)
            chunks.append(sentence.split(' '))
    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])
    res = summarizer(chunks, max_length=120, min_length=30, do_sample=False)
    ' '.join([summ['summary_text'] for summ in res])
    text = ' '.join([summ['summary_text'] for summ in res])
    return text

def summarizer(ARTICLE):
    summarizer = pipeline("summarization")
    max_chunk = 500

    ARTICLE = ARTICLE.replace('.', '.<eos>')
    ARTICLE = ARTICLE.replace('?', '?<eos>')
    ARTICLE = ARTICLE.replace('!', '!<eos>')

    sentences = ARTICLE.split('<eos>')
    current_chunk = 0 
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            print(current_chunk)
            chunks.append(sentence.split(' '))
    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])
    res = summarizer(chunks, max_length=120, min_length=30, do_sample=False)
    ' '.join([summ['summary_text'] for summ in res])
    text = ' '.join([summ['summary_text'] for summ in res])
    return text

def sentiment_analysis(text):
    sentiment_analysis = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
    return sentiment_analysis(text)

def question_answering(context, question):
    '''Pass the question from the user input and all the transcript in memory as context'''
    qa_model = pipeline("question-answering")
    answer = qa_model(question = question, context = context)
    return answer

def zero_shot_classification(sequence_to_classify,candidate_labels):
    classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
    results = classifier(sequence_to_classify, candidate_labels)
    return results

def zero_shot_classification_overtime_(sequence_to_classify,candidate_labels):
    candidate_labels = str(candidate_labels).split(', ')
    candidate_labels = [label.strip(' ') for label in candidate_labels]
    classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli", )
    results = []
    # divide sequesce into chunks of size 100
    for i in range(0, len(sequence_to_classify), len(sequence_to_classify)//10):
        result = classifier(sequence_to_classify[i:i+len(sequence_to_classify)//10], candidate_labels)
        scores = result['scores']
        results.append([scores[i] for i in range(len(candidate_labels))])
    results = pd.DataFrame(results, columns=candidate_labels)
    print(results)
    # create graph
    fig = px.line(results, x=range(len(results)), y=candidate_labels, height=500, width=800)
    return fig

###########
def zero_shot_classification_overtime(sequence_to_classify,candidate_labels):
    candidate_labels = str(candidate_labels).split(', ')
    candidate_labels = [label.strip(' ') for label in candidate_labels]
    classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli", )
    results = []
    # divide sequesce into chunks of size 100
    for i in range(0, len(sequence_to_classify), len(sequence_to_classify)//10):
        result = classifier(sequence_to_classify[i:i+len(sequence_to_classify)//10], candidate_labels)
        scores = result['scores']
        results.append([scores[i] for i in range(len(candidate_labels))])
    results = pd.DataFrame(results, columns=candidate_labels)
    print(results)
    # create graph
    fig = px.line(results, x=range(len(results)), y=candidate_labels, height=500, width=800)
    return fig
