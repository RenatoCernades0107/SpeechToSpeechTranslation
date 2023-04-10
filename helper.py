import pandas as pd
import re

def clear_voices_name_csv():
    df = pd.read_csv('database/voices_name.csv', sep=';', header=None).dropna()

    df.loc[:,1] = pd.Series([l.split(' ')[0] for l in df[1]])

    unique_languages = df[1].unique()

    df2 = pd.DataFrame({})

    for l in unique_languages:
        df2 = pd.concat([df2, df[df[1] == l].head(1)])

    df2.loc[:,2] = pd.Series([re.split(r"\d|['(']",l)[0].strip() for l in df2[2]])
    df2.to_csv("languages/voices_name.csv",header=True)

def clear_recognition_languages():
    df = pd.read_csv('database/recognition_languages.csv', sep=';', header=None).dropna()
    df.to_csv("languages/recognition_languages.csv",header=True)

def clear_target_languages():
    df = pd.read_csv('database/target_languages.csv', sep=';', header=None).dropna()
    df.loc[:,0] = pd.Series([re.split(r"['(']",l)[0].replace(' ','') for l in df[0]])
    df.to_csv("languages/target_languages.csv",header=True)

def match_target_and_voice():
    df_tl = pd.read_csv('languages/target_languages.csv', sep=',',header=0, index_col=0)
    df_vn = pd.read_csv('languages/voices_name.csv', sep=',',header=0, index_col=0)

    df = pd.DataFrame({})
    unique_languages = df_tl["0"].unique()

    for l in unique_languages:
        row_df = df_tl[df_tl["0"] == l]
        try:
            match_row = df_vn[df_vn["1"] == l]["2"].unique()[0]
            row_df.insert(2, "voice", match_row)
            df = pd.concat([df, row_df])
        except Exception as e:
            print(e)
    
    df.dropna().to_csv("languages/voice_and_target_languages.csv",header=True)
    


if __name__ == "__main__":
    clear_voices_name_csv()
    clear_recognition_languages()
    clear_target_languages()

    match_target_and_voice()
