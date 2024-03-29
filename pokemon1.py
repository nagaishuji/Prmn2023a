import streamlit as st
import pandas as pd

df = pd.read_csv('data/pokemon_data.csv', index_col='id')

st.title("ポケモン図鑑")
st.caption("ポケモンのいずれかの情報を入力してください")

# 検索方法の選択
search_option = st.radio("検索方法を選択してください", ["図鑑番号", "名前", "タイプ"])

# フォームの開始
with st.form("my_form"):
    if search_option == "図鑑番号":
        number = st.number_input("ポケモンの図鑑番号(1～1010)を入力", min_value=1, max_value=1010)
    elif search_option == "タイプ":
        type_option = st.radio("検索方法を選択してください(ノーマル、ほのお、みず、でんき、くさ、こおり、かくとう、どく、じめん、ひこう、エスパー、むし、いわ、ゴースト、ドラゴン、あく、はがね、フェアリー)", ["片方のタイプで検索", "両方のタイプで検索"])

        if type_option == "片方のタイプで検索":
            type_input = st.text_input("ポケモンのタイプを入力")
            selected_row = df[(df['タイプ1'] == type_input) | (df['タイプ2'] == type_input)]
        else:
            type_input_1 = st.text_input("ポケモンのタイプ1つめを入力")
            type_input_2 = st.text_input("ポケモンのタイプ2つめを入力")
            selected_row = df[
                ((df['タイプ1'] == type_input_1) & (df['タイプ2'] == type_input_2)) |
                ((df['タイプ1'] == type_input_2) & (df['タイプ2'] == type_input_1))
            ]
    else:
        input_text = st.text_input("ポケモンの名前を入力")

    # submitボタンの生成
    submitted = st.form_submit_button("検索")

# submitボタンが押されたときの処理
if submitted:
    if search_option == "図鑑番号":
        selected_row = df[df.index == number]
    elif search_option == "タイプ":
        if type_option == "片方のタイプで検索":
            selected_row = df[(df['タイプ1'] == type_input) | (df['タイプ2'] == type_input)]
        else:
            selected_row = df[
                ((df['タイプ1'] == type_input_1) & (df['タイプ2'] == type_input_2)) |
                ((df['タイプ1'] == type_input_2) & (df['タイプ2'] == type_input_1))
            ]
    else:
        selected_row = df[df['名前'].str.lower() == input_text.lower()]

    if not selected_row.empty:
        st.write("選択されたポケモンの情報:")
        st.write(selected_row)
    else:
        st.write("該当するポケモンが見つかりませんでした。")
