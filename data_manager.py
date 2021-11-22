'''
ACL18 [31], KDD17 은 공공 datasets이다. ([9]에서 사용됨)
위 URL에서 사전 처리된(preprocessed) 버전을 가져오고, 동일하게 training, validation, and test splits를 사용했다.
https://github.com/fulifeng/Adv-ALSTM

요건
input : 데이터(구체적으로 확인하기)
output : 전처리 필요
- feature column 만들기
   ; chart_data 만들 필요가 없음
- 
'''
# 모듈 import
import pandas as pd
import numpy as np
import os
from datetime import datetime

# raw data path 지정
raw_data_path = './Adv-ALSTM/data/stocknet-dataset/price/raw'

# feature data path 지정
feature_data_path = './Adv-ALSTM/data/stocknet-dataset/price/feature'

# 파일명 저장
fnames = [fname for fname in os.listdir(raw_data_path) if
            os.path.isfile(os.path.join(raw_data_path,fname))]

# feature column
COLUMNS_FEATURE_DATA_V1 = ['open_close_ratio', 'high_close_ratio', 
                           'low_close_ratio', 'close_lastclose_ratio', 
                           'adjclose_lastadjclose_ratio', 'close_ma5_ratio', 
                           'close_ma10_ratio', 'close_ma15_ratio', 'close_ma20_ratio', 
                           'close_ma25_ratio', 'close_ma30_ratio']

# moveing average windows
windows = [5,10,15,20,25,30]

def preprocess(df, windows):
   '''
   전처리 함수 역할 : 전체 feature생성하여 df column에 추가
   csv저장
   '''
   data = df
   data['open_close_ratio'] = data['Open'] / data['Close'] - 1
   data['high_close_ratio'] = data['High'] / data['Close'] - 1
   data['low_close_ratio'] = data['Low'] / data['Close'] - 1

   data['close_lastclose_ratio'] = np.zeros(len(data))
   data.loc[1:, 'close_lastclose_ratio'] = data['Close'][1:].values / data['Close'][:-1].values - 1

   data['adjclose_lastadjclose_ratio'] = np.zeros(len(data))
   data.loc[1:, 'adjclose_lastadjclose_ratio'] = data['Adj Close'][1:].values / data['Adj Close'][:-1].values - 1

   for window in windows:
      data[f'close_ma{window}_ratio'] = data['Close'].rolling(window).mean()/data['Close'] - 1

   return data


def load_data(raw_data_path, feature_data_path, date_from, date_to, ver='v1'):
   # raw 파일에서 티커명 저장
   fnames = [fname for fname in os.listdir(raw_data_path) if
            os.path.isfile(os.path.join(raw_data_path,fname))]

   # feature 추가된 csv 파일 없으면 저장
   for fname in fnames:
      if not os.path.isfile(os.path.join(feature_data_path,fname)):
         df_raw = pd.read_csv(os.path.join(raw_data_path,fname))
         data = preprocess(df_raw, windows)

         # 폴더 없으면 생성
         try:
            if not os.path.exists(feature_data_path):
               os.makedirs(feature_data_path)
         except OSError:
            print ('Error: Creating directory. ' +  feature_data_path)

         #csv 파일 저장
         data.to_csv(os.path.join(feature_data_path,fname))   




