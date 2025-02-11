import pandas as pd
import random

# Excel dosyasını okuma
file_path = "is_ilanları_son.xlsx"
df = pd.read_excel(file_path)

# Uzaktan/Normal sütunundaki değerleri değiştirme
df["Uzaktan/Normal"] = df["Uzaktan/Normal"].replace({
    "hybrid": "hibrit",
    "hibrit": "hibrit",
    "uzaktan": "uzaktan",
    "Uzaktan / Remote": "uzaktan",
    "remote": "uzaktan",
    "iş yerinde": "iş yerinde"
})

# '$' işareti içeren hücreleri kontrol et ve değerini değiştir
df["Uzaktan/Normal"] = df["Uzaktan/Normal"].apply(
    lambda x: random.choice(["iş yerinde", "uzaktan", "hibrit"]) if isinstance(x, str) and "$" in x else x
)

# Çalışma Şekli sütunundaki değerleri değiştirme
df["Çalışma Şekli"] = df["Çalışma Şekli"].replace({
    "uzaktan": random.choice(["tam zamanlı", "yarı zamanlı", "sözleşmeli", "stajyer"]),
    "hybrid": random.choice(["tam zamanlı", "yarı zamanlı", "sözleşmeli", "stajyer"]),
    "orta-üst düzey yönetici": random.choice(["tam zamanlı", "yarı zamanlı", "sözleşmeli", "stajyer"]),
    "dönemsel": "sözleşmeli",
    "proje bazlı": "sözleşmeli",
    "full-time": "tam zamanlı",
    "Dönemsel / Proje Bazlı": "sözleşmeli",
    "Yarı Zamanlı / Part Time": "yarı zamanlı"
})

# Tüm hücrelerdeki metinleri küçük harfe çevirme ve fazla boşlukları temizleme
df = df.apply(lambda col: col.str.strip().str.lower() if col.dtype == "object" else col)

df["Uzaktan/Normal"] = df["Uzaktan/Normal"].replace({
    "hybrid": "hibrit",
    "hibrit": "hibrit",
    "uzaktan": "uzaktan",
    "Uzaktan / Remote": "uzaktan",
    "remote": "uzaktan",
    "iş yerinde": "iş yerinde"
})


# Çalışma Şekli sütunundaki değerleri değiştirme
df["Çalışma Şekli"] = df["Çalışma Şekli"].replace({
    "uzaktan": random.choice(["tam zamanlı", "yarı zamanlı", "sözleşmeli", "stajyer"]),
    "hybrid": random.choice(["tam zamanlı", "yarı zamanlı", "sözleşmeli", "stajyer"]),
    "orta-üst düzey yönetici": random.choice(["tam zamanlı", "yarı zamanlı", "sözleşmeli", "stajyer"]),
    "dönemsel": "sözleşmeli",
    "proje bazlı": "sözleşmeli",
    "full-time": "tam zamanlı",
    "dönemsel / proje bazlı": "sözleşmeli",
    "yarı zamanlı / part time": "yarı zamanlı"
})

# Boş hücreleri doldurma işlemi: "İstenen Tecrübe" hariç
for column in df.columns:
    if column != "İstenen Tecrübe" and df[column].dtype == "object":
        df[column] = df[column].fillna("belirtilmemiş")

# Düzenlenmiş dosyayı kaydetme
output_path = "is_ilanları_son_cleaned.xlsx"
df.to_excel(output_path, index=False)

print(f"Veri ön işleme tamamlandı ve dosya '{output_path}' olarak kaydedildi.")
