import pandas as pd

# Dosyayı yükleme
dosya_adi = "is_ilanları_son_cleaned.xlsx"
data = pd.read_excel(dosya_adi)

# "Uzaktan/Normal" sütunundaki belirtilmemiş değerleri dengeleme
if "Uzaktan/Normal" in data.columns:
    uzaktan_normal_values = ["iş yerinde", "hibrit", "uzaktan"]
    belirtilmemis_count = (data["Uzaktan/Normal"] == "belirtilmemiş").sum()
    mevcut_sayilar = data["Uzaktan/Normal"].value_counts().to_dict()

    # Eksik değerleri dengeleyecek şekilde dağıtma
    for i, index in enumerate(data[data["Uzaktan/Normal"] == "belirtilmemiş"].index):
        yeni_deger = uzaktan_normal_values[i % len(uzaktan_normal_values)]
        data.at[index, "Uzaktan/Normal"] = yeni_deger

# "Çalışma Şekli" sütunundaki belirtilmemiş değerleri dengeleme
if "Çalışma Şekli" in data.columns:
    calisma_sekli_values = ["yarı zamanlı", "sözleşmeli", "stajyer"]
    belirtilmemis_count = (data["Çalışma Şekli"] == "belirtilmemiş").sum()
    mevcut_sayilar = data["Çalışma Şekli"].value_counts().to_dict()

    # Eksik değerleri dengeleyecek şekilde dağıtma
    for i, index in enumerate(data[data["Çalışma Şekli"] == "belirtilmemiş"].index):
        yeni_deger = calisma_sekli_values[i % len(calisma_sekli_values)]
        data.at[index, "Çalışma Şekli"] = yeni_deger

# "İstenen Tecrübe" sütunundaki boş hücreleri 0 ile doldurma
if "İstenen Tecrübe" in data.columns:
    data["İstenen Tecrübe"] = data["İstenen Tecrübe"].apply(
        lambda x: 0 if (pd.isna(x) or (isinstance(x, str) and x.strip() == "")) else x
    )


# "Eğitim Seviyesi" sütunundaki belirtilmemiş değerleri boş bırakma
if "Eğitim Seviyesi" in data.columns:
    data["Eğitim Seviyesi"] = data["Eğitim Seviyesi"].replace("belirtilmemiş", "")

# Düzenlenmiş dosyayı kaydetme
duzenlenmis_dosya_adi = "is_ilanlari_son_cleaned_duzenlenmis.xlsx"
data.to_excel(duzenlenmis_dosya_adi, index=False)

print(f"Düzenlemeler tamamlandı. Dosya kaydedildi: {duzenlenmis_dosya_adi}")
