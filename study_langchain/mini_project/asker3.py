from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, FewShotChatMessagePromptTemplate, load_prompt
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from dotenv import load_dotenv

def few_shot_prompt():

    examples = [
        {
            "question": "I'm searching for a sunscreen which my baby and I could use.",
            "answer": """
        The product I would like to recommend is the following:

        Brand name: CURE
        Product name: Aqua Mild Green Sun Cream
        Features:
        - Contains 42% aloe vera leaf juice for gentle, soothing care.
        - Suitable for both adults and babies, offering mild protection.
        - Free from harsh chemicals, making it safe for sensitive skin.
        - Lightweight formula that absorbs easily and is simple to cleanse
        
        This sunscreen is perfect for you and your baby—gentle, soothing, and easy to apply. The aloe vera keeps skin calm and hydrated without feeling heavy. Safe, lightweight, and great for sensitive skin! 
    """
        }]

    # index 객체 생성
    index = faiss.IndexFlatL2(len(examples))

    # vectorstore 객체 생성
    examples_vectorstore = FAISS(
        embedding_function=OpenAIEmbeddings(),
        index=index,
        docstore=InMemoryDocstore(), # 문서 저장소. 메모리상(로컬 아님)
        index_to_docstore_id={}
    )

    # SemanticSimilarityExampleSelector 생성
    example_selector2 = SemanticSimilarityExampleSelector.from_examples(
        # 선택 가능한 예시 목록
        examples,
        # 유사도 확인을 위한 임베딩 클래스 제공
        OpenAIEmbeddings(),
        # vector값을 저장할 db 지정
        examples_vectorstore,
        # 생성할 예시 개수
        k=1
    )

    example_prompt = ChatPromptTemplate.from_messages(
            [
                ('human', '{question}'),
                ('ai','{answer}')
            ]
        )

    return FewShotChatMessagePromptTemplate(
        example_selector=example_selector2,
        example_prompt=example_prompt)

def generate_prompt_from_file(txt_file_path, template_file_path):
    """
    텍스트 파일을 읽고 템플릿에 삽입하여 프롬프트를 생성하는 함수.
    
    Parameters:
    - txt_file_path (str): 텍스트 파일의 경로
    - template_file_path (str): 프롬프트 템플릿 파일의 경로
    
    Returns:
    - prompt (str): 텍스트가 삽입된 프롬프트 문자열
    """
    # 텍스트 파일에서 내용 읽기
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        youtube_subtitles = txt_file.read()
    
    # 템플릿 파일에서 템플릿 로드 및 텍스트 삽입
    prompt_template = load_prompt(template_file_path, encoding='utf-8')
    prompt = prompt_template.format(youtube_subtitles=youtube_subtitles)
    
    return prompt

# ChatPromptTemplate 작성
def ask_gpt(user_input):
    
    prompt = generate_prompt_from_file('study_langchain/mini_project/cosmetics_recommendation.txt', 'study_langchain/mini_project/prompt_template.yaml')

    final_prompt = ChatPromptTemplate.from_messages([
        ('system', """
    당신은 뷰티 온라인몰에서 English speaking 외국 고객을 상대로 맞춤형 화장품을 추천해주는 친근하면서도 똑똑한 AI 상담사입니다.
    고객님의 피부 고민에 맞는 화장품을 매칭해주세요.

    매칭할 화장품은 한국 유명 유튜브 인플루언서 "디렉터 파이"의 추천 정보를 바탕으로 합니다.
    모든 상담은 영어로 진행되며, 답안은 고객이 직관적으로 이해하기 쉽게 설명합니다.
         
    마지막으로, 추천하는 제품은 유튜브 인플루언서가 추천한 제품 한에서만 추천하세요.
    유튜버의 추천 정보 중에 고객님의 요청사항에 맞게 추천해 줄만한 제품이 없으면 없다고 분명히 기재하되, 유투버가 추천한 다른 제품을 대체품으로 제시하세요.
        """),
        few_shot_prompt(),
        ('human', prompt),
        ('human', '{user_input}')
    ])

    return final_prompt.format_messages(user_input=user_input)

def answer_by_gpt2(user_input):
    load_dotenv()    
    model = ChatOpenAI(model='gpt-4', temperature=0)
    ai_message = ask_gpt(user_input=user_input)

    return model.invoke(ai_message).content