import pytest
from websploit.app import create_connection, get_cached_file_path, save_cached_file_path, clear_cache, download_sqlite_file, select_exploits_by_keywords
import sqlite3
import os
import tempfile
import requests

@pytest.fixture
def setup_cache_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    save_cached_file_path(temp_file.name)
    yield temp_file.name
    if os.path.exists(temp_file.name):
        os.remove(temp_file.name)
    if os.path.exists("cached_sqlite_file_path.txt"):
        os.remove("cached_sqlite_file_path.txt")

def test_create_connection(setup_cache_file):
    conn = create_connection()
    assert isinstance(conn, sqlite3.Connection)
    conn.close()

def test_get_cached_file_path(setup_cache_file):
    cached_file_path = get_cached_file_path()
    assert cached_file_path == setup_cache_file

def test_clear_cache(setup_cache_file):
    clear_cache()
    assert not os.path.exists(setup_cache_file)
    assert get_cached_file_path() is 1

def test_download_sqlite_file(monkeypatch):
    # モックURLとレスポンスを作成
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, content):
                self.content = content
                self.status_code = 200

            def json(self):
                return self.content
        return MockResponse(b"test content")
    
    monkeypatch.setattr(requests, "get", mock_get)
    downloaded_file_path = download_sqlite_file()
    assert os.path.exists(downloaded_file_path)
    os.remove(downloaded_file_path)

def test_select_exploits_by_keywords():
    # テスト用のデータベース接続
    conn = sqlite3.connect(':memory:')
    conn.execute('CREATE TABLE exploits (exploit_type TEXT, cve_id TEXT, description TEXT, url TEXT)')
    conn.execute("INSERT INTO exploits VALUES ('type1', 'CVE-1234', 'Exploit 1', 'url1')")
    conn.execute("INSERT INTO exploits VALUES ('type2', 'CVE-5678', 'Exploit 2', 'url2')")
    conn.execute("INSERT INTO exploits VALUES ('type3', 'CVE-91011', 'Exploit 3', 'url3')")

    # ヒットする場合のテスト
    keywords = ["Exploit", "CVE-1234"]
    result = select_exploits_by_keywords(conn, keywords)
    assert not result.empty
    assert "CVE-1234" in result.index
    assert len(result) == 1

    keywords = ["Exploit 3"]
    result = select_exploits_by_keywords(conn, keywords)
    assert not result.empty
    assert "CVE-91011" in result.index
    assert len(result) == 1

    # ヒットしない場合のテスト
    keywords = ["Nonexistent"]
    result = select_exploits_by_keywords(conn, keywords)
    assert result.empty
 
    keywords = ["Nonexistent", "Keyword"]
    result = select_exploits_by_keywords(conn, keywords)
    assert result.empty

    keywords = ["url3"]
    result = select_exploits_by_keywords(conn, keywords)
    assert result.empty

# def test_url_availability():
#     url =  "https://this-is-test-bucket-tf-my.s3.ap-northeast-1.amazonaws.com/go-exploitdb.sqlite3"
#     assert check_url_availability(url) == True

def check_url_availability(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False