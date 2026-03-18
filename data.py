import pandas as pd
df = pd.read_csv("Healthcare_data.csv")

print(df.duplicated().sum())
df = df.drop_duplicates()
print(df.duplicated().sum())
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

df = df[(df["age"] > 0) & (df["age"] <= 120)]

df["calculated_symptom_count"] = df["symptoms"].apply(lambda x: len(x.split(",")))
df = df[df["symptom_count"] == df["calculated_symptom_count"]]

df.drop(columns=["calculated_symptom_count"], inplace=True)


for col in df.columns:
    if df[col].dtype in ["int64", "float64"]:
        df[col] = df[col].fillna(df[col].median())
    else:
        df[col] = df[col].fillna(df[col].mode()[0])

for col in df.select_dtypes(include="object"):
    df[col] = df[col].str.strip()

print(df.groupby("disease")["age"].mean())
print(df["disease"].value_counts())

def get_age_group(age):
    if age<=12:
        return "Child"
    elif age<=19:
        return "Teen"
    elif age<=60:
        return "Adult"
    else:
        return "Senior"
    


df["age_group"]=df["age"].apply(get_age_group)

print("No of rows")

print(df.count())

df.to_csv("Healthcare_Transformed.csv", index=False)