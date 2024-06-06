import csv
import requests
from tqdm import tqdm

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

def to_float(s):
    if s is None or s == '':
        return

    return float(s.replace(",",""))

def to_int(s):
    if s is None or s == '':
        return

    return int(s.replace(",",""))

def to_good_not_good(rank):
    try:
        rank = int(rank)

        if rank == 1:
            return "좋음"
        elif rank == 2:
            return "보통"
        else:
            return "미흡"
    except:
        return None

def to_high_low(rank):
    try:
        rank = int(rank)

        if rank == 1:
            return "높음"
        elif rank == 2:
            return "보통"
        else:
            return "낮음"
    except:
        return None


def to_up_down(rank):
    try:
        rank = int(rank)

        if rank == 1:
            return "상승"
        elif rank == 2:
            return "유지"
        else:
            return "하락"
    except:
        return None


def get_fund_full_info(fund_summary):
    fund_full_info = {}
    fund_full_info["FUND_CD"] = fund_summary["FUND_CD"]
    fund_full_info["FUND_NM"] = fund_summary["FUND_NM"]
    fund_full_info["HASHTAG"] = fund_summary["HASHTAG"]
    fund_full_info["STD_PRC"] = to_float(fund_summary["STD_PRC"])
    fund_full_info["DIFF_PRC"] = to_float(fund_summary["DIFF_PRC"])
    fund_full_info["DRV_NAV"] = to_float(fund_summary["DRV_NAV"])
    fund_full_info["PRNK_FUND_NAV_1D"] = to_float(fund_summary["PRNK_FUND_NAV_1D"])
    fund_full_info["SET_DT"] = fund_summary["SET_DT"]
    fund_full_info["RT_1M"] = to_float(fund_summary["RT_1M"])
    fund_full_info["RT_3M"] = to_float(fund_summary["RT_3M"])
    fund_full_info["RT_6M"] = to_float(fund_summary["RT_6M"])
    fund_full_info["RT_YTD"] =to_float(fund_summary["RT_YTD"])
    fund_full_info["RT_1Y"] = to_float(fund_summary["RT_1Y"])
    fund_full_info["RT_3Y"] = to_float(fund_summary["RT_3Y"])
    fund_full_info["RT_5Y"] = to_float(fund_summary["RT_5Y"])
    fund_full_info["TER"] = to_float(fund_summary["TER"])
    fund_full_info["RISK_GRADE"] = to_int(fund_summary["RISK_GRADE"])
    fund_full_info["RISK_GRADE_TXT"] = fund_summary["RISK_GRADE_TXT"]

    fund_code = fund_summary["FUND_CD"]

    fund_info_response = requests.get("https://www.fundguide.net/Api/Fund/GetFundInfo", {
        "fund_cd": fund_code,
        "_": "1717592772566"
    })

    if fund_info_response.status_code == 200:
        fund_info = fund_info_response.json()["Data"]
        fund_full_info["CO_NM"] = fund_info[0][0]["CO_NM"]
        fund_full_info["FEE_GB"] = fund_info[0][0]["FEE_GB"]
        fund_full_info["CLA_URL"] = fund_info[0][0]["CLA_URL"]
        fund_full_info["INV_URL"] = fund_info[0][0]["INV_URL"]
        fund_full_info["PEER_CD_L_NM"] = fund_info[0][0]["PEER_CD_L_NM"]
        fund_full_info["PEER_CD_NM"] = fund_info[0][0]["PEER_CD_NM"]
        fund_full_info["DRV_SET_AMT"] = to_int(fund_info[0][0]["DRV_SET_AMT"])

        fund_full_info["MANAGER"] = fund_info[1][0]["MANGR"] #철자가 이럼
        fund_full_info["CUSTODY_NM"] = fund_info[1][0]["CUSTODY_NM"]
        fund_full_info["BACK_NM"] = fund_info[1][0]["BACK_NM"]
        fund_full_info["INFO_OBJECT"] = fund_info[1][0]["INFO_OBJECT"]
        fund_full_info["INFO_STRATEGY"] = fund_info[1][0]["INFO_STRATEGY"]
        fund_full_info["REF_BM"] = fund_info[1][0]["REF_BM"]
        fund_full_info["REGION"] = fund_info[1][0]["REGION"]

        fund_full_info["AMT_GB"] = to_up_down(fund_info[0][0]["AMT_GB"])
        fund_full_info["EXCE_BM"] = to_good_not_good(fund_info[0][0]["EXCE_BM"])
        fund_full_info["RISK_GB"] = to_high_low(fund_info[0][0]["RISK_GB"])
        fund_full_info["RT_GB"] = to_good_not_good(fund_info[0][0]["RT_GB"])
        fund_full_info["SMALL_SCALE_YN"] = fund_info[0][0]["SMALL_SCALE_YN"]
    else:
        print(f"Fail Get Fund Portfolio by {fund_code}")


    fund_portfolio_response = requests.get("https://www.fundguide.net/Api/Fund/GetFundPortfolio", {
        "fund_cd": fund_code,
        "_": "1717592772566"
    })

    if fund_portfolio_response.status_code == 200:
        fund_portfolio = fund_portfolio_response.json()["Data"][0][0]

        fund_full_info["STOCK_FRG_RT"] = to_float(fund_portfolio["STOCK_FRG_RT"])
        fund_full_info["STOCK_RT"] = to_float(fund_portfolio["STOCK_RT"])
        fund_full_info["BOND_FRG_RT"] = to_float(fund_portfolio["BOND_FRG_RT"])
        fund_full_info["BOND_RT"] = to_float(fund_portfolio["BOND_RT"])
        fund_full_info["INVEST_RT"] = to_float(fund_portfolio["INVEST_RT"])
        fund_full_info["ETC_RT"] = to_float(fund_portfolio["ETC_RT"])

        fund_full_info["PEER_STOCK_FRG_RT"] = to_float(fund_portfolio["PEER_STOCK_FRG_RT"])
        fund_full_info["PEER_STOCK_RT"] = to_float(fund_portfolio["PEER_STOCK_RT"])
        fund_full_info["PEER_BOND_FRG_RT"] = to_float(fund_portfolio["PEER_BOND_FRG_RT"])
        fund_full_info["PEER_BOND_RT"] = to_float(fund_portfolio["PEER_BOND_RT"])
        fund_full_info["PEER_INVEST_RT"] = to_float(fund_portfolio["PEER_INVEST_RT"])
        fund_full_info["PEER_ETC_RT"] = to_float(fund_portfolio["PEER_ETC_RT"])
    else:
        print(f"Fail Get Fund Portfolio by {fund_code}")

    return fund_full_info

def fund_crawling(sel_co, sel_peer, count=4):
    search_payload = {
        "selPeer": sel_peer,
        "selCo": sel_co,
        "listCondFr": "0.00|0.00",
        "listCondNm": "수탁고|총보수율",
        "listCondTo": "121,201.76|73.58",
        "listCondGroup": "C|B",
        "listCondIndex": "1|2",
        "listCondOption": "1|1",
        "listCondSeq": "2|1",
        "sort_col": "RT_1Y", #수익률,
        "ord_gb": "DESC",
        "page_no": "1",
        "row_cnt": count,
        "_": "1717514798096"

    }

    fund_list_response = requests.get("https://www.fundguide.net/Api/Fund/GetFundList", search_payload)

    if fund_list_response.status_code == 200:
        fund_list = fund_list_response.json()["Data"][0]

        fund_result_list = []
        for fund_summary in fund_list:
            fund_info = get_fund_full_info(fund_summary)
            fund_result_list.append(fund_info)

        return fund_result_list

    return []

if __name__ == '__main__':
    # 펀드 운용사 301(미래에셋), 210(신한자산운용), 105(삼성자산운용), 223(KB자산운용)
    sel_co_list = ["301", "210", "105", "223"]

    # 국내주식 HS001|HSA01|HSAG1|HSAM1|HSAD1
    # 국내 혼합형: HM001|HMA01|HMS01|HMB01|HMBM1|HMBA1|HMBH1
    # 해외 주식: FS001|FSC01|FSCJ1|FSCC1|FSCI1|FSCV1|FSCB1|FSCR1|FSCO1|FSS01|FSSE1|FSSM1|FSSH1|FSSF1|FSSI1|FSSP1|FSSC1|FSSN1|FSSO1|FSR01|FSRG1|FSRD1|FSRM1|FSRU1|FSRE1|FSRN1|FSRS1|FSRP1|FSRX1|FSRA1|FSRI1|FSRO1|FSO01
    # 해외 혼합: FM001|FMA01|FMAD1|FMS01|FMB01|FMO01
    # 해외 채권: FB001|FBG01|FBGB1|FBGH1|FBR01|FBRM1|FBRP1|FBRN1|FBRS1|FBRU1|FBO01
    sel_peer_list = [
        "HS001|HSA01|HSAG1|HSAM1|HSAD1",
        "HM001|HMA01|HMS01|HMB01|HMBM1|HMBA1|HMBH1",
        "FS001|FSC01|FSCJ1|FSCC1|FSCI1|FSCV1|FSCB1|FSCR1|FSCO1|FSS01|FSSE1|FSSM1|FSSH1|FSSF1|FSSI1|FSSP1|FSSC1|FSSN1|FSSO1|FSR01|FSRG1|FSRD1|FSRM1|FSRU1|FSRE1|FSRN1|FSRS1|FSRP1|FSRX1|FSRA1|FSRI1|FSRO1|FSO01",
        "FM001|FMA01|FMAD1|FMS01|FMB01|FMO01",
        "FB001|FBG01|FBGB1|FBGH1|FBR01|FBRM1|FBRP1|FBRN1|FBRS1|FBRU1|FBO01"
    ]

    fund_list = []

    for sel_co in tqdm(sel_co_list):
        for sel_peer in sel_peer_list:
            fund_list.extend(fund_crawling(sel_co, sel_peer, 5))


    with open('fund.csv', 'w') as f:
        field_names = fund_list[0].keys()
        w = csv.DictWriter(f, fieldnames=field_names)

        w.writeheader()
        w.writerows(fund_list)

        f.close()

    print(f"Num of Data: {len(fund_list)}")

