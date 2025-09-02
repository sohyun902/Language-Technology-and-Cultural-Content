from functions.naver_crawler import search_naver_blogs, extract_blog_content
from functions.sentiment_analyzer import load_model
from functions.scorer import classify_and_score_reviews
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')
warnings.filterwarnings("ignore", category=FutureWarning)

def main():
    # 모델 불러오기
    lr_model, tfidf_vectorizer = load_model()
    if lr_model is None or tfidf_vectorizer is None:
        return 
    
    # API 호출
    client_id = "YOUR_NAVER_CLIENT_ID"
    client_secret = "YOUR_NAVER_CLIENT_SECRET"

    # 영화 리뷰 탐색
    movie_title = input("영화제목을 입력하세요: ")
    blog_links = search_naver_blogs(client_id, client_secret, movie_title)
    if not blog_links:
        print("No blog links found.")
        return

    blog_contents = extract_blog_content(blog_links)
    if not blog_contents:
        print("No blog content extracted.")
        return

    # 평점 계산
    avg_story_score, avg_expression_score = classify_and_score_reviews(blog_contents, lr_model, tfidf_vectorizer)

    # 결과물 출력
    print(f"\n{movie_title}의 연출 점수는 {avg_expression_score}입니다")
    print(f"{movie_title}의 스토리 점수는 {avg_story_score}입니다")

if __name__ == "__main__":

    main()
