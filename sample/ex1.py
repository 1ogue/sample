import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# 데이터 불러오기
data = pd.read_csv('서울시도서관정보.csv', encoding='utf-8')

# 필요한 컬럼 추출
data = data[['대출 가능권수', '소재지(시군구)', '도서관유형']]

# 결측치 제거
data = data.dropna()

# 데이터 전처리
le = LabelEncoder()
data['소재지(시군구)_인코딩'] = le.fit_transform(data['소재지(시군구)'])
data['도서관유형_인코딩'] = le.fit_transform(data['도서관유형'])

# 독립 변수(X)와 종속 변수(y)로 데이터 분리
X = data[['대출 가능권수', '소재지(시군구)_인코딩', '도서관유형_인코딩']]
y = data['도서관유형']

# 학습 데이터와 테스트 데이터로 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 로지스틱 회귀 모델 학습
model = LogisticRegression()
model.fit(X_train, y_train)

# 테스트 데이터로 예측
y_pred = model.predict(X_test)

# 예측 결과 출력
print(y_pred)
