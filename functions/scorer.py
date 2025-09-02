from functions.sentiment_analyzer import analyze_sentiment, preprocess_and_tokenize

story_keywords = ["스토리", "이야기", "내용", "줄거리", "개연성", "결말", "서사", "대사"]
expression_keywords = ["연출", "OST", "ost", "음악", "영상미", "효과음", "CG", "cg","Cg","편집", "트랙", "작화", "씬", "액션"]

# 문장 유형 분류
def classify_and_score_reviews(contents, model, vectorizer):
    processed_contents = preprocess_and_tokenize(contents)

    all_story_sents = []
    all_expression_sents = []

    for doc_sents in processed_contents:
        story_sents_doc = []
        expression_sents_doc = []
        for sent in doc_sents:
            if any(keyword in sent for keyword in story_keywords):
                story_sents_doc.append(sent)
            if any(keyword in sent for keyword in expression_keywords):
                expression_sents_doc.append(sent)
        all_story_sents.extend(story_sents_doc)
        all_expression_sents.extend(expression_sents_doc)

    story_predictions = analyze_sentiment(all_story_sents, model, vectorizer)
    expression_predictions = analyze_sentiment(all_expression_sents, model, vectorizer)

    avg_story_score = calculate_score(story_predictions)
    avg_expression_score = calculate_score(expression_predictions)

    return avg_story_score, avg_expression_score

# 점수 계산
def calculate_score(predictions):
    if predictions.size == 0:
        return 0.0 

    positive_count = sum(predictions)
    negative_count = len(predictions) - positive_count

    if positive_count + negative_count == 0:
        return 0.0

    score = (positive_count / (positive_count + negative_count)) * 10
    return round(score, 2)