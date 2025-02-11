import pandas as pd
import random

# Excel dosyalarını oku
df1 = pd.read_excel("is_ilanlari_son_cleaned_duzenlenmis.xlsx")
df2 = pd.read_excel("yeteneklerle_guncellenmis_cv.xlsx")

# Yeni bir DataFrame oluştur
result = pd.DataFrame()

# İlgili sütunları kaldır
if 'POZİSYON ADI' in df2.columns:
    df2 = df2.drop(columns=['POZİSYON ADI', 'BAŞLANGIÇ - BİTİŞ TARİHİ', 'BÖLÜM ADI', 'MEZUNİYET TARİHİ', 
                            'VEREN KURULUŞ', 'İÇERİK', 'GÖNÜLLÜLÜK ROLÜ', 'GÖNÜLLÜ PROJE/YAPILAN İŞ', 'DENEYİM SÜRESİ'])

if 'İlan Adı' in df1.columns:
    df1 = df1.drop(columns=['İlan Adı', 'Sektör', 'Şirket', 'Detay', ' Tecrübe'])

# Maksimum kombinasyon sayısı
max_combinations = 100000
row_count = 0

# Rastgele eşleştirme için index listeleri
df1_indices = list(df1.index)
df2_indices = list(df2.index)

# Kombinasyonları oluştur
while row_count < max_combinations:
    i = random.choice(df1_indices)
    j = random.choice(df2_indices)
    
    # İlgili satırları birleştir
    combined_row = pd.concat([df1.iloc[[i]], df2.iloc[[j]]], ignore_index=True)
    result = pd.concat([result, combined_row], ignore_index=True)
    
    row_count += 1
    if row_count % 1000 == 0:
        print(f"{row_count} satır işlendi...")

# Sonucu yeni bir dosyaya yaz
result.to_excel("birlesmis_excel_100k.xlsx", index=False)
print("Birleştirme işlemi tamamlandı, birlesmis_excel_100k.xlsx dosyası oluşturuldu.")