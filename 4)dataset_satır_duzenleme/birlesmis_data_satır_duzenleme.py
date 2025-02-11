import pandas as pd

# Excel dosyasını yükle
file_path = "/content/birlesmis_excel_100k.xlsx"  # Excel dosyanızın tam yolunu buraya yazın
data = pd.read_excel(file_path)

# Yeni bir DataFrame oluştur
merged_rows = []
columns_1 = ["Uzaktan/Normal", "Çalışma Şekli", "Yetenekler", "Konum", "İstenen Tecrübe", "Eğitim Seviyesi"]
columns_2 = ["DERECE", "ÖNE ÇIKAN PROJE", "SERTİFİKA ADI", "YETENEKLER", "DİL", "GÖNÜLLÜLÜK YAPTIĞI ORGANİZASYON ADI", "konum", "Çalışma Şekli2", "Çalışma Türü", "ÇALIŞMA ZAMANI (YIL)"]

# Satırları kontrol ederek birleştir
for i in range(len(data) - 1):
    row1 = data.iloc[i]
    row2 = data.iloc[i + 1]

    # Eğer birinci satır columns_1 sütunlarına, ikinci satır columns_2 sütunlarına sahipse
    if not row1[columns_1].isnull().all() and not row2[columns_2].isnull().all():
        # İki satırı birleştir
        merged_row = row1.combine_first(row2)
        merged_rows.append(merged_row)

# Yeni DataFrame oluştur
merged_df = pd.DataFrame(merged_rows)

# Yeni dosyayı kaydet
output_file = "merged_output.xlsx"
merged_df.to_excel(output_file, index=False)

print(f"Birleştirilmiş veriler '{output_file}' olarak kaydedildi.")