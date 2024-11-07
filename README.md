1. 소개 및 기획 배경
A. 프로젝트 목표
이 프로젝트는 한국 화장품을 구매하려는 외국인 고객을 대상으로, 한국 인플루언서 추천 정보를 기반으로 개인화된 화장품을 추천하는 챗봇 시스템을 구축하는 것입니다. 사용자의 요구에 맞는 제품을 추천해 고객이 더 쉽고 빠르게 제품을 선택할 수 있도록 돕습니다.

B. 기획 배경
이 시스템은 실제 경험을 바탕으로 기획되었습니다. 한국에 온 교환학생들에게 화장품을 추천할 때, 한국 현지인의 추천 정보가 대부분 한국어로 제공되어 접근이 어려운 문제를 경험했습니다. 또한, 외국인 고객들이 한국 화장품을 선호하는 경향이 있어, 언어 장벽을 해결할 필요성을 느꼈습니다.

따라서, 한국인 인플루언서의 추천 정보를 영어로 변환하여, 외국인 고객에게 적합한 화장품을 추천하는 시스템을 기획하였습니다. 이를 통해 외국인 관광객들이 한국 화장품을 더 쉽게 선택하고, 구매 결정을 돕는 역할을 할 것으로 기대됩니다.


### System Architecture Diagram


```mermaid
graph LR
    User -->|Input Query| StreamlitUI[Streamlit UI]
    StreamlitUI -->|Invoke function| answer_by_gpt2
    answer_by_gpt2 -->|Generate prompt| OpenAIAPI[OpenAI API]
    OpenAIAPI -->|Return response| answer_by_gpt2
    answer_by_gpt2 -->|Display response| StreamlitUI
    StreamlitUI -->|Store conversation| SessionState[Session State]
    StreamlitUI -->|Display to user| User
