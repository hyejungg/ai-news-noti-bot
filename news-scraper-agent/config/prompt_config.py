class DefaultPromptTemplate:
    CRAWLING_AGENT_PROMPT_EN = """<Roles and objectives>
Please find the articles by extracting information from the html based on the information below 

<Context>
The site information is as follows.
- Site name: {site_name}
- Site link: {site_url}
- html: {parser_result}

<Instructions>
1. Make sure to extract information from the html that is delivered.
2. If additional information is available, use the additional information to extract the article title and website link.
3. The extracted information should not be changed arbitrarily.
4. The answer must be in JSON array form, responding to the article title and the article's website link in key-value form as follows.
5. If the article information has not been imported, respond in the form of an empty array: ex. '[]'
6. If the url is not a full url starting with a protocol(http, https), use relative paths based on the provided site link to convert it into a complete url.
7. If the site name is 데보션(Devocean), exclude the content corresponding to Geeknews.
8. If the site name is 긱뉴스, refer to the href of the a tag for the url, prioritizing the article address within 긱뉴스.
9. Be sure to follow the instructions above.
"""

    CRAWLING_AGENT_PROMPT_KO = """<역할 및 목표>
아래 정보를 바탕으로 html에서 아티클을 찾아주세요

<문맥>
사이트 정보는 다음과 같습니다.
- 사이트 이름: {site_name}
- 사이트 링크: {site_url}
- html: {parser_result}

<지시문>
1. 반드시 전달되는 html 내에서 정보를 추출합니다.
2. 추가 정보가 있는 경우 추가 정보를 활용하여 기사 제목과 웹사이트 링크를 추출합니다.
3. 추출한 정보를 임의로 변경해선 안됩니다.
4. 답변은 반드시 JSON 배열 형태로 기사 제목(title)과 기사의 웹사이트 링크(url)를 다음과 같은 key-value 형태로 응답합니다.
5. 기사 정보를 못가져 온 경우 다음과 같이 빈 배열 형태로 응답합니다. ex. '[]'
6. 주소가 프로토콜(http, https)로 시작하는 전체 url이 아닌 경우 제공된 사이트 링크를 기준으로 상대경로를 사용하여 완전한 url로 변환하여 사용하세요.
7. 사이트 이름이 데보션(devocean)인 경우, Geeknews에 해당하는 내용은 제외하세요
8. 사이트 이름이 긱뉴스인 경우, url은 a 태그의 href를 참조하되 긱뉴스 내 아티클주소를 우선시합니다. 
9. 반드시 위 지침을 따르세요.
"""

    # filtering llm agent prompt
    FILTERING_AGENT_PROMPT_EN = """<Role & Goal>
The tool aims to filter AI-related news articles, focusing on the latest AI technologies and research trends, generative AI, AI application domains, notable AI use cases, and the societal and economic impacts of AI.

<Context>
{crawling_result}

<Instructions>
1. From the given list of news articles, filter only those related to AI and output them in JSON format. Each article object should include only the 'title' and 'url' attributes.
2. The main keywords are as follows:
    - AI Technology and Research Keywords: 'LLM,' 'Generative AI,' 'AI,' 'Deep Learning,' 'Machine Learning,' 'Natural Language Processing' (NLP), 'Reinforcement Learning,' 'Transformers,' 'Language Model,' 'Neural Network,' 'Classification Model,' 'Clustering,' 'Regression Analysis,' 'Time Series Analysis'
    - Generative AI Keywords: 'Generative Model,' 'Image Generation,' 'Text Generation,' 'Speech Recognition,' 'Image Recognition,' 'Computer Vision,' 'Natural Language Generation' (NLG), 'Generative Adversarial Networks' (GAN), 'Natural Language Understanding,' 'Multimodal AI'
    - Application Fields and Use Cases: 'Recommendation Systems,' 'Automation,' 'Chatbot,' 'Healthcare AI,' 'Finance AI,' 'Robotics,' 'Smart Home,' 'Autonomous Driving,' 'Edge Computing,' 'Cloud AI'
    - AI Technology and Research Trends: 'AI Ethics,' 'Explainable AI,' 'AI Safety,' 'Model Compression,' 'Scalability,' 'Large-Scale Training,' 'Hyperparameters,' 'Lightweight Models,' 'Model Optimization,' 'Transfer Learning'
    - Unique AI Applications: 'Client-side AI,' 'Browser-based AI,' 'Experimental AI,' 'AI Service,' 'AI solutions for developers,' 'Novel AI applications'
    - Societal and Economic Impact Keywords: 'AI Regulation', 'AI Policy', 'Social Impact of AI', 'Job Impact', 'Economics of AI', 'AI Market Growth', 'AI Investment', 'Industry Disruption', 'Future Technology', 'AI Innovation', 'Future of AI', 'AI Competition', 'AI Leadership'
3. Output the results in JSON format following the given format.
"""

    FILTERING_AGENT_PROMPT_KO = """<역할 및 목표>
AI 관련 뉴스 기사를 필터링하는 도구로서, 최신 AI 기술과 연구 동향, 생성형 AI, AI 응용 분야, 특별한 AI 응용 사례, 그리고 AI의 사회적, 경제적 영향 등을 다루는 기사만을 추출하는 것이 목표입니다.

<문맥>
{crawling_result}

<지시문>
1. 주어진 뉴스 목록에서 AI와 관련된 기사만 필터링하여 JSON 형식으로 출력하세요. 각 기사 객체에는 'title'과 'url' 속성만 포함합니다.
2. 주요 키워드는 다음과 같습니다:
    - AI 기술 및 연구 관련 키워드 : 'LLM', '생성형 AI', 'AI', '딥러닝' (Deep Learning), '머신러닝' (Machine Learning), '자연어 처리' (NLP, Natural Language Processing), '강화 학습' (Reinforcement Learning), '트랜스포머' (Transformers), '언어 모델' (Language Model), '신경망' (Neural Network), '분류 모델' (Classification Model), '군집화' (Clustering), '회귀 분석' (Regression Analysis), '시계열 분석' (Time Series Analysis)
    - 생성형 AI 관련 키워드 : '생성 모델' (Generative Model), '이미지 생성' (Image Generation), '텍스트 생성' (Text Generation), '음성 인식' (Speech Recognition), '이미지 인식' (Image Recognition), '컴퓨터 비전' (Computer Vision), '자연어 생성' (NLG, Natural Language Generation), 'GAN' (Generative Adversarial Networks), '자연어 이해' (Natural Language Understanding), '멀티모달 AI' (Multimodal AI)
    - 응용 분야와 사례 : '추천 시스템' (Recommendation Systems), '자동화' (Automation), '챗봇' (Chatbot), '의료 AI' (Healthcare AI), '금융 AI' (Finance AI), '로보틱스' (Robotics), '스마트 홈' (Smart Home), '자율 주행' (Autonomous Driving), '엣지 컴퓨팅' (Edge Computing), '클라우드 AI' (Cloud AI)
    - AI 기술 및 연구 동향 : 'AI 윤리' (AI Ethics), '설명 가능한 AI' (Explainable AI), 'AI 안전성' (AI Safety), '모델 압축' (Model Compression), '확장성' (Scalability), '대규모 학습' (Large-Scale Training), '하이퍼파라미터' (Hyperparameters), '경량화 모델' (Lightweight Models), '모델 최적화' (Model Optimization), '전이 학습' (Transfer Learning)
    - AI 응용 : '클라이언트 측 AI' (Client-side AI), '브라우저 기반 AI' (Browser-based AI), '실험적 AI' (Experimental AI), 'AI 서비스' (AI Service), '개발자를 위한 AI 솔루션' (AI solutions for developers), '신규 AI 애플리케이션' (Novel AI applications)
    - AI의 사회적 및 경제적 시사점 관련 키워드: 'AI 규제' (AI Regulation), 'AI 정책' (AI Policy), 'AI의 사회적 영향' (Social Impact of AI), '일자리 영향' (Job Impact), 'AI 경제학' (Economics of AI), 'AI 시장 성장' (AI Market Growth), 'AI 투자' (AI Investment), '산업 변화' (Industry Disruption), '미래 기술' (Future Technology), 'AI 혁신' (AI Innovation), '미래 AI' (Future of AI), 'AI 경쟁' (AI Competition), 'AI 리더십' (AI Leadership)"
3. JSON 형식으로 주어진 형식에 맞게 출력하세요.
"""

    # sorting llm agent prompt
    SORTING_AGENT_PROMPT_EN = """<Role and Objective>
As a tool for ranking AI-related news articles by importance, the goal is to evaluate each article's significance based on practical applications of AI, the latest technological trends, creative use cases, and tangible benefits for developers and users.

<Context>
{filtering_result}

<Instructions>
1. Rank the given list of news articles in order of importance.
2. Do not modify or restructure the provided list of articles arbitrarily.
3. Evaluate the importance of each article based on the following criteria (higher rank indicates greater importance):
    - **1st Priority: Practical AI Applications** : Articles showcasing AI technologies that are commercialized to solve problems or improve user experience.
    - **2nd Priority: Latest AI Technological Trends** : Articles covering advancements in AI technology, performance improvements, or research-driven insights.
    - **3rd Priority: Latest AI Development Frameworks** : Articles about AI management frameworks, developer tools, or techniques such as RAG or fine-tuning.
    - **4th Priority: Creative and Innovative Use Cases** : Articles demonstrating novel or fun applications of AI, showcasing new possibilities or creative implementations.
    - **5th Priority: Social Impact and Policy Relevance** : Articles discussing AI-related legislation, policies, or contributions to solving societal challenges.
    - **6th Priority: Industrial Scalability and Investment Trends** : Articles addressing AI's expansion into new industries, investments, or business growth.
4. Output the results following the given format in JSON.
    - id: included id in the request
    - reason: the category of evaluation criteria this article falls under (e.g., Latest AI Technological Trends)
"""

    SORTING_AGENT_PROMPT_KO = """<역할 및 목표>
AI 관련 뉴스 기사를 중요도에 따라 정렬하는 도구로서, AI의 실질적 활용 사례, 최신 기술 트렌드, 창의적 활용, 개발자와 사용자에게 실질적 이점을 제공하는 요소를 고려해 기사의 중요도를 평가하는 것이 목표입니다.

<문맥>
{filtering_result}

<지시문>
1. 주어진 뉴스 목록에서 각 기사를 중요도에 따라 순서대로 정렬하세요.
2. 임의로 뉴스 목록을 수정하거나 재구성하지 않습니다.
3. 중요도를 평가하는 기준은 다음과 같습니다 (순위가 높을수록 중요도가 높음):
    - **1순위: 실질적인 AI 기술 활용 사례** : AI 기술이 상용화되어 문제를 해결하거나 사용자 경험을 개선하는 기사
    - **2순위: 최신 AI 기술 트렌드** : 최신 AI 기술의 발전 방향, 성능 개선, 연구 중심의 내용을 다룬 기사
    - **3순위: 최신 AI 개발 프레임워크** : 최신 I 관리 프레임워크나 개발자 도구, AI 활용 기법 (RAG, 파인튜닝 등)에 대한 기사
    - **4순위: 창의적이고 혁신적인 활용 사례** : 기존과 다른 창의적인 방식으로 AI를 응용하여 새로운 가능성을 보여주거나 재미있는 활용 사례에 대한 기사.
    - **5순위: 사회적 영향 및 정책적 중요성** : AI 관련 입법, 정책, 사회 문제 해결 사례를 다룬 기사.
    - **6순위: 산업적 확장성 및 투자 동향** : AI 기술의 확장성, 투자 및 신사업 관련 내용을 다룬 기사.
4. JSON 형식으로 주어진 형식에 맞게 출력하세요.
    - id: 요청에 포함된 id
    - reason: 이 기사가 포함되는 평가 기준 카테고리 (예: 최신 AI 기술 트렌드 등)
"""
