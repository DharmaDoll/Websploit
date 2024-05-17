import streamlit as st
import sqlite3
import pandas as pd
from sqlite3 import Error
import shlex

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("/home/taro/Kev/data/go-exploitdb.sqlite3")
    except Error as e:
        print(e)

    return conn

def select_articles_by_keywords(conn, keywords):
    params = [f"%{keyword.strip()}%" for keyword in keywords for _ in range(2)]
    query = 'SELECT exploit_type, cve_id, description, url FROM exploits'
    query += ' WHERE ' + ' AND '.join('(description LIKE ? OR cve_id LIKE ?)' for keyword in keywords)
    df = pd.read_sql_query(query, conn, params=params)
    df = df.set_index(['cve_id'])
    return df

def main():
    st.set_page_config(layout="wide")
    st.sidebar.title("Keyword Search")
    user_input = st.sidebar.text_input("Enter keywords(cve_id, description) separated by space", value='"Windows Server 2012 R2" code exec')
    try:
        keywords = shlex.split(user_input)  # parse the user input
        if st.sidebar.button("Search"):
            conn = create_connection()
            if conn is not None:
                result = select_articles_by_keywords(conn, keywords)
                st.write(f"Results found: {len(result)}")
                st.dataframe(result.sort_index(ascending=False), height=1000, width=1300)
    except ValueError:
        st.error("Input Error: Make sure your keywords or phrases (double quoted) are properly formatted.")


if __name__ == "__main__":
    main() 
