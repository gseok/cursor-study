#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KBO 홈페이지 팀 순위 스크래핑 스크립트
URL: https://www.koreabaseball.com/Default.aspx
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class KBOTeamRankingScraper:
    """KBO 팀 순위 정보를 스크래핑하는 클래스"""
    
    def __init__(self, use_selenium=True):
        self.base_url = "https://www.koreabaseball.com/Default.aspx"
        self.use_selenium = use_selenium
        self.driver = None
        
        if not use_selenium:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            self.session = requests.Session()
            self.session.headers.update(self.headers)
    
    def setup_driver(self):
        """Selenium WebDriver 설정"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 브라우저 창을 띄우지 않음
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            return True
        except Exception as e:
            print(f"WebDriver 설정 실패: {e}")
            return False
    
    def fetch_page(self):
        """웹페이지를 가져오는 메서드"""
        if self.use_selenium:
            return self.fetch_page_selenium()
        else:
            return self.fetch_page_requests()
    
    def fetch_page_selenium(self):
        """Selenium을 사용하여 웹페이지를 가져오는 메서드"""
        try:
            if not self.driver:
                if not self.setup_driver():
                    return None
            
            print(f"KBO 홈페이지에 접속 중... ({self.base_url})")
            self.driver.get(self.base_url)
            
            # 페이지가 완전히 로드될 때까지 대기
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, "tblTeamRank")))
            
            # 추가 대기 시간 (JavaScript 실행 완료를 위해)
            time.sleep(3)
            
            print("페이지 로드 완료!")
            return self.driver.page_source
            
        except Exception as e:
            print(f"웹페이지 로드 실패: {e}")
            return None
    
    def fetch_page_requests(self):
        """requests를 사용하여 웹페이지를 가져오는 메서드"""
        try:
            print(f"KBO 홈페이지에 접속 중... ({self.base_url})")
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            print("페이지 로드 완료!")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"웹페이지 로드 실패: {e}")
            return None
    
    def parse_team_ranking(self, html_content):
        """팀 순위 정보를 파싱하는 메서드"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 팀 순위 테이블 찾기
        team_ranking_table = soup.find('table', {'id': 'tblTeamRank'})
        
        if not team_ranking_table:
            print("팀 순위 테이블을 찾을 수 없습니다.")
            return None
        
        # 기준 날짜 추출
        date_element = soup.find('p', {'id': 'lblTeamRank'})
        date_text = date_element.get_text(strip=True) if date_element else "날짜 정보 없음"
        
        # 테이블 데이터 추출
        tbody = team_ranking_table.find('tbody')
        if not tbody:
            print("팀 순위 테이블의 tbody를 찾을 수 없습니다.")
            return None
        
        teams_data = []
        rows = tbody.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['th', 'td'])
            if len(cells) >= 9:  # 순위, 팀명, 경기, 승, 패, 무, 승률, 게임차, 연속
                team_data = {
                    '순위': cells[0].get_text(strip=True),
                    '팀명': cells[1].find('span', class_='team-name').get_text(strip=True) if cells[1].find('span', class_='team-name') else cells[1].get_text(strip=True),
                    '경기': cells[2].get_text(strip=True),
                    '승': cells[3].get_text(strip=True),
                    '패': cells[4].get_text(strip=True),
                    '무': cells[5].get_text(strip=True),
                    '승률': cells[6].get_text(strip=True),
                    '게임차': cells[7].get_text(strip=True),
                    '연속': cells[8].get_text(strip=True)
                }
                teams_data.append(team_data)
        
        return {
            '기준_날짜': date_text,
            '팀_순위': teams_data,
            '스크래핑_시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def display_ranking(self, ranking_data):
        """순위 정보를 보기 좋게 출력하는 메서드"""
        if not ranking_data:
            print("표시할 순위 데이터가 없습니다.")
            return
        
        print("\n" + "="*80)
        print(f"🏆 KBO 팀 순위 ({ranking_data['기준_날짜']})")
        print("="*80)
        print(f"{'순위':<4} {'팀명':<6} {'경기':<4} {'승':<3} {'패':<3} {'무':<3} {'승률':<6} {'게임차':<6} {'연속':<6}")
        print("-"*80)
        
        for team in ranking_data['팀_순위']:
            print(f"{team['순위']:<4} {team['팀명']:<6} {team['경기']:<4} {team['승']:<3} {team['패']:<3} {team['무']:<3} {team['승률']:<6} {team['게임차']:<6} {team['연속']:<6}")
        
        print("="*80)
        print(f"📅 스크래핑 시간: {ranking_data['스크래핑_시간']}")
        print("="*80)
    
    def save_to_json(self, ranking_data, filename=None):
        """순위 데이터를 JSON 파일로 저장하는 메서드"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"kbo_team_ranking_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(ranking_data, f, ensure_ascii=False, indent=2)
            print(f"📁 데이터가 {filename} 파일로 저장되었습니다.")
        except Exception as e:
            print(f"파일 저장 실패: {e}")
    
    def run(self):
        """메인 실행 메서드"""
        print("🚀 KBO 팀 순위 스크래핑을 시작합니다...")
        
        # 웹페이지 가져오기
        html_content = self.fetch_page()
        if not html_content:
            return False
        
        # 팀 순위 파싱
        ranking_data = self.parse_team_ranking(html_content)
        if not ranking_data:
            return False
        
        # 결과 출력
        self.display_ranking(ranking_data)
        
        # JSON 파일로 저장
        self.save_to_json(ranking_data)
        
        return True
    
    def cleanup(self):
        """리소스 정리"""
        if self.driver:
            self.driver.quit()
            self.driver = None


def main():
    """메인 함수"""
    scraper = KBOTeamRankingScraper()
    
    try:
        success = scraper.run()
        if success:
            print("\n✅ 스크래핑이 성공적으로 완료되었습니다!")
        else:
            print("\n❌ 스크래핑 중 오류가 발생했습니다.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  사용자에 의해 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")
        sys.exit(1)
    finally:
        scraper.cleanup()


if __name__ == "__main__":
    main()
