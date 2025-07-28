from flask import jsonify, request
import praw
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from os import environ
from sentiment import bp

# Reddit API setup
reddit = praw.Reddit(
    client_id=environ.get("REDDIT_ID"),
    client_secret=environ.get("REDDIT_SECRET"),
    user_agent="mod-sentiment-analyzer",
)

# HuggingFace sentiment pipeline (RoBERTa)
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


def clean_text(text):
    return re.sub(r"\s+", " ", text.strip())


def analyze_single_module(module_name):
    results = []
    subreddit = reddit.subreddit("nus+nusmods")

    for post in subreddit.search(module_name, limit=5):
        results.append(clean_text(post.title + " " + post.selftext)[:500])
        post.comments.replace_more(limit=0)
        for comment in post.comments[:5]:
            results.append(clean_text(comment.body)[:500])

    if not results:
        return {
            "module": module_name,
            "total_comments": 0,
            "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0},
            "sample_comments": [],
        }

    scores = classifier(results, truncation=True)

    sentiment_scores = {"LABEL_0": 0, "LABEL_1": 0, "LABEL_2": 0}
    for res in scores:
        label = res["label"]
        sentiment_scores[label] += 1

    total = sum(sentiment_scores.values())
    sentiment_percentages = {
        label.lower(): round((count / total) * 100, 2)
        for label, count in sentiment_scores.items()
    }

    return {
        "module": module_name,
        "total_comments": total,
        "sentiment_distribution": sentiment_percentages,
        "sample_comments": results[:5],
    }


@bp.route("/sentiment/bert", methods=["POST"])
def analyze_modules():
    data = request.get_json()
    module_list = data.get("modules", [])

    results = []
    for mod in module_list:
        try:
            result = analyze_single_module(mod)
        except Exception as e:
            result = {"module": mod, "error": str(e)}
        results.append(result)

    return jsonify(results)
