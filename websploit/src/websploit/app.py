import streamlit as st
import sqlite3
import pandas as pd
from sqlite3 import Error
import requests
import shlex
import tempfile
import os

CACHE_FILE_PATH_STORAGE = "cached_sqlite_file_path.txt"

def create_connection():
    conn = None
    try:
        cache_file_path = get_cached_file_path()
        if cache_file_path is None:
            cache_file_path = download_sqlite_file()
            save_cached_file_path(cache_file_path)
            print(f"Downloaded and cached SQLite file at {cache_file_path}")  
        else:
            print(f"Using cached SQLite file at {cache_file_path}") 
        conn = sqlite3.connect(cache_file_path)
    except Error as e:
        print(e)
    return conn

def get_cached_file_path():
    if os.path.exists(CACHE_FILE_PATH_STORAGE):
        with open(CACHE_FILE_PATH_STORAGE, 'r') as file:
            path = file.read().strip()
            if os.path.exists(path):
                return path
    return None

def save_cached_file_path(path):
    with open(CACHE_FILE_PATH_STORAGE, 'w') as file:
        file.write(path)

def clear_cache():
    if os.path.exists(CACHE_FILE_PATH_STORAGE):
        with open(CACHE_FILE_PATH_STORAGE, 'r') as file:
            path = file.read().strip()
            if os.path.exists(path):
                os.remove(path)
        os.remove(CACHE_FILE_PATH_STORAGE)
    st.sidebar.success("Cache cleared!")

def download_sqlite_file():
    sqlite_url = "https://this-is-test-bucket-tf-my.s3.ap-northeast-1.amazonaws.com/go-exploitdb.sqlite3"
    response = requests.get(sqlite_url)
    if response.status_code == 200:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite3")
        with open(temp_file.name, 'wb') as f:
            f.write(response.content)
        return temp_file.name
    else:
        raise ConnectionError("Failed to download SQLite file")

def select_exploits_by_keywords(conn, keywords):
    params = [f"%{keyword.strip()}%" for keyword in keywords for _ in range(2)]
    query = 'SELECT exploit_type, cve_id, description, url FROM exploits'
    query += ' WHERE ' + ' AND '.join('(description LIKE ? OR cve_id LIKE ?)' for keyword in keywords)
    df = pd.read_sql_query(query, conn, params=params)
    df = df.set_index(['cve_id'])
    return df

def main():
    st.set_page_config(layout="wide")
    st.sidebar.title("Keyword Search")

    # http://localhost:8501/?btn=true
    params = st.experimental_get_query_params()
    if params.get("btn", [None])[0] == "true":
        if st.sidebar.button("Clear Cache"):
            clear_cache()

    user_input = st.sidebar.text_input("Enter keywords(cve_id, description) separated by space", value='"Windows Server 2012 R2" code exec')
    try:
        keywords = shlex.split(user_input)  # parse the user input
        if st.sidebar.button("Search"):
            conn = create_connection()
            if conn is not None:
                result = select_exploits_by_keywords(conn, keywords)
                st.write(f"Results found: {len(result)}")
                st.dataframe(result.sort_index(ascending=False), height=1000, width=1300)
    except ValueError:
        st.error("Input Error: Make sure your keywords or phrases (double quoted) are properly formatted.")
    except ConnectionError as e:
        st.error(f"Connection Error: {e}")

if __name__ == "__main__":
    main() 

