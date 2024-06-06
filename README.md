# 펀드 크롤러
작성자: 김동원   
참고 사이트: [펀드가이드](https://www.fundguide.net/)

## 구동 방법
`requests / tqdm` 라이브러리 필요   
`main.py` 실행
- 현재 기준은 미래에셋 / 신한 / KB / 삼성 자산운용사에서 수익률이 가장 좋은 국내 주식 / 국내 혼합형 / 해외 주식 / 해외 혼합 / 해외 채권 펀드들을 5개씩 가져온 결과 입니다.
- 약 1~2분 정도 소요 (100개 수집)
- 만약 크롤링된 결과를 보고 싶으시면 `fund.csv`를 참고해주세요
## 데이터 형식
```python
# Fund 데이터 양식
# FUND_CD(펀드 고유번호): 'K55301DS3146'
# FUND_NM(펀드 이름): '미래에셋TIGER필라델피아반도체레버리지증권상장지수투자신탁(주식혼합-파생형)(합성)'
# HASHTAG(해시태그): '#해외주식형#ETF(해외주식)#레버리지#레버리지#북미'
# STD_PRC(기준가(원)): 26382.79
# DIFF_PRC(기준가에서 오른 원화?): 291.54
# DRV_NAV(운용규모(억원)): 2266.28
# PRNK_FUND_NAV_1D(운용규모 상위 몇 %): 20.45
# SET_DT(설정일): '2022.04.14'
# RT_1M(수익률 %(1달)): 26.77
# RT_3M(수익률 %(3달)): 12.45
# RT_6M(수익률 %(6달)): 100.88
# RT_YTD(수익률 %(연초)): 62.02
# RT_1Y(수익률 %(1년)): 115.56
# RT_3Y(수익률 %(3년)): 111
# RT_5Y(수익률 %(5년)): 111
# TER(총보수(%)): 0.67
# RISK_GRADE(위험등급(숫자)): 1
# RISK_GRADE_TXT(위험등급(텍스트)): '매우 높은 위험'

# CO_NM (운용사): '미래에셋자산운용'
# FEE_GB (수수료): '선취(X),후취(X),환매(X)'
# CLA_URL (집합투자규약 pdf url): "http:&#47;&#47;file.fnguide.com&#47;upload1&#47;FnSpectrum&#47;invest&#47;K55301DS3146_약.pdf"
# INV_URL (투자설명서 pdf url): "http://file.fnguide.com/upload1/FnSpectrum/invest/K55301DS3146_약.pdf"
# PEER_CD_L_NM(펀드 유형 1) : "해외주식형"
# PEER_CD_NM(펀드 유형 2) : "정보기술섹터"
# MANAGER (매니저) : "김지연"
# CUSTODY_NM (수탁은행) : "한국시티은행"
# BACK_NM (사무관리회사) : "한국펀드파트너스"
# INFO_OBJECT (투자목적) : "이 투자신탁은 주식관련 파생상품 및 집합투자증권을 법 시행령 제94조제2항제4호에서 규정하는 주된 투자대상자산으로 하며, 미국 주식으로 구성된 PHLX Semiconductor Sector 지수(원화환산)를 기초지수로하여 1좌당 순자산가치의 일간변 동률을 기초지수 일간변동률의 양의 2배수로 연동하여 투자신탁재산을 운용함을 목적으로 합니다."
# INFO_STRATEGY (투자전략) : "이 투자신탁은 Nasdaq에서 발표하는 PHLX Semiconductor Sector 지수(원화환산)를 기초지수로 하여 기초지수의 일간 수익률의 양의 2배수 수익률과 연동하는 것을 목적으로 하는 상장지수투자신탁으로서, 기초지수관련 파생상품(스왑) 및 집합투자증권을 주된 투자대상으로 하여 투자신탁의 일간수익률이 기초지수 일간수익률의 양의 2배수 수익률과 연동하도록 운용합니다."
# REF_BM (비교지수): "PHLX Semiconductor Sector Leveraged Index(원화환산) * 100%"
# REGION (투자지역): "북미&#47;북미"
# DRV_SET_AMT (판드규모(설정액(억원))) : 859

# AMT_GB (규모성장): 상승/유지/하락
# EXCE_BM (BM초과성과) 좋음/보통/미흡
# RISK_GB (위험도): 높음/보통/낮음
# RT_GB (성과지속): 좋음/보통/미흡
# SMALL_SCALE_YN (소규모 펀드): N/Y
# <!-- [개발] summ1 : 좋음 / summ2 : 보통 / summ3 : 미흡 / up1 : 상승 / up2 : 유지 / up3 : 하락 /
# high1 : 높음 / high2 : 보통 / high3 : 낮음 / summ_y : 소규모 펀드 / summ_n : 소규모 펀드 없음 -->

# 포트폴리오 (자산 구성(펀드))
# STOCK_FRG_RT (해외주식): 0
# STOCK_RT (국내주식): 0
# BOND_FRG_RT (해외채권):0
# BOND_RT (국내채권): 0
# ETC_RT (기타) : 1.24
# INVEST_RT(수익 증권) : 98.76

# 포트폴리오 (자산구성(유형 평균))
# PEER_BOND_FRG_RT(해외채권) : 0.02
# PEER_BOND_RT (국내채권): 0.00
# PEER_ETC_RT(기타) : 6.88
# PEER_INVEST_RT (수익증권): 32.48
# PEER_STOCK_FRG_RT (해외주식): 59.39
# PEER_STOCK_RT (주식): 1.23
```