import pandas as pd
import re
import random

# Excel dosyasının yolunu belirleyin
excel_dosyasi = r"C:\Users\beyza\OneDrive\Masaüstü\cv_new.xlsx"

# Excel dosyasını yükleyin
df = pd.read_excel(excel_dosyasi)

# Dereceleri belirli kategorilerle eşleştirmek için bir sözlük oluşturuyoruz
dereceler = {
    'Lisans': ['Lisans', 'Bachelor', 'B.Sc', 'B.A.', 'B.S.', 'Bachelors', 'Bachelors of Science', 'Bachelor of Science', 
               'Bachelor’s', 'BSc', 'B.A', 'B.Sc.', 'BSc.', 'Bachelor of Arts', 'Bachelor of Engineering', 'B.Tech', 
               'B.Sc. (Hons)', 'B.Com (Onur)', 'BBA', 'Bachelor of Engineering', 'Bachelor of Technology'],
    'Önlisans': ['Önlisans', 'Associates', 'Associate', 'AA', 'A.A.', 'Associate Degree', 'Associates Degree', 
                  'Associate of Applied Science', 'Associate of Science', 'A.S.', 'A.A.S.'],
    'Lisansüstü': ['Lisansüstü', 'Master', 'Master’s', 'M.Sc', 'M.S.', 'M.A.', 'Master of Science', 'Master of Arts', 
                   'MSc', 'M.A.', 'Master of Legal Studies', 'M.S', 'M.Sc.', 'M.S.', 'MBA', 'Executive MBA'],
    'Yüksek Lisans': ['Yüksek Lisans', 'Yüksek Lisans Diploması', 'Fen Bilimleri Yüksek Lisansı', 'İşletme Yüksek Lisansı', 
                      'Bilgi Sistemleri Yüksek Lisansı', 'Fen Yüksek Lisansı', 'Teknoloji Yüksek Lisansı'],
    'Sertifika': ['Sertifika', 'Certification', 'Diploma', 'Meslek Yüksekokulu Diploması', 'Mesleki Sertifika', 
                  'Postgraduate Certificate', 'Certifications', 'Sertifika Programı'],
    'Doktora': ['Doktora', 'Ph.D.', 'Doctorate']
}

# Fonksiyon, hücredeki değeri doğru dereceye dönüştürür
def replace_degrees(value):
    value = str(value)  # Değeri metin formatına dönüştür
    if any(alias in value for alias in dereceler['Yüksek Lisans']):
        return 'Yüksek Lisans'
    elif any(alias in value for alias in dereceler['Lisans']):
        return 'Lisans'
    for degree, aliases in dereceler.items():
        if any(alias in value for alias in aliases):
            return degree
    return 'Belirtilmemiş'

# Tarih temizleme fonksiyonu (güncellenmiş)
def temizle_tarih(value):
    value = re.sub(r'\(.*\)', '', str(value)).strip()  # Parantez içindekileri kaldır
    value = re.sub(r'\b(\d{2})\/(\d{4})\b', r'\2', value)  # '12/2014' gibi tarihleri sadece yıl haline getir
    value = re.sub(r'^\d{5}$', lambda x: x.group()[1:], value)  # 5 haneli sayılar
    value = re.sub(r'^\d{6}$', lambda x: x.group()[2:], value)  # 6 haneli sayılar
    value = re.sub(r'(January|February|March|April|May|June|July|August|September|October|November|December|Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)', '', value, flags=re.IGNORECASE).strip()  # Ay isimlerini kaldır
    value = re.sub(r'(- Devam Ediyor|- Halen|Devam Ediyor|Halen)', '', value, flags=re.IGNORECASE).strip()  # Ay isimlerini kaldır
    value = re.sub(r'^\d{2}\.(\d{4})$', r'\1', value)  # Ay ve yıl formatını sadece yıl olarak bırak
    value = re.sub(r'\bıs\s*(\d{4})\b', r'\1', value)  # 'ıs' ile ayrılan tarihleri yıl haline getir
    
    
    # ';' varsa ',' ile değiştiriyoruz
    value = value.replace(';', ',')
    
    value = value.replace('.', ',')  # Noktayı virgülle değiştir
    
    # Tarih belirtilmemiş ise
    if 'Tarih belirtilmemiş' in value or '-' in value or 'Beirtilmemiş' in value or 'Present' in value or not value:
        return 'Belirtilmemiş'
    return value


# Mezuniyet yılı ile deneyim süresi hesaplama fonksiyonu (güncellenmiş)
def deneyim_suresi_hesapla(value):
    if 'devam ediyor' in value.lower() or 'belirtilmemiş' in value.lower() or 'present' in value.lower():
        return 0
    
    # Yılları virgülle ayırarak liste haline getiriyoruz
    yillar = value.split(',')
    
    # Yılları temizliyoruz ve en büyük yılı alıyoruz
    temizlik_yillari = [int(temizle_tarih(yil.strip())) for yil in yillar if yil.strip().isdigit()]
    
    if temizlik_yillari:
        # En büyük yılı alıyoruz ve 2025'ten çıkarıyoruz
        en_buyuk_yil = max(temizlik_yillari)
        deneyim_suresi = 2025 - en_buyuk_yil
        
        # Eğer deneyim süresi 20'den büyükse, 1-10 arasında rastgele bir deneyim süresi atıyoruz
        if deneyim_suresi > 17:
            return random.randint(1, 10)
        
        return deneyim_suresi
    return 0  # Eğer yıl bilgisi yoksa 0 döndür
# Tarih temizleme fonksiyonu
def temizle_baslangic_bitis(value):
    # Eğer boş veya eksik bir değer varsa
    if not value or pd.isna(value):
        return 'Belirtilmemiş'
    
    # Baştaki ve sondaki boşlukları sil
    value = value.strip()
    
    # Veriyi virgülle ayır
    tarih_listesi = str(value).split(',')
    temiz_tarih_listesi = []
    
    for tarih in tarih_listesi:
        # Her bir tarihi işleme al
        tarih = tarih.strip()  # Başındaki ve sonundaki boşlukları temizle
        tarih = re.sub(r'\(.*?\)|\(.*', '', str(tarih)).strip()
        tarih = re.sub(r'^.*\)', '', str(tarih)).strip()

        # 'present', 'halen devam ediyor' vb. ifadeleri 2020 olarak değiştir
        tarih = re.sub(r'(present|halen devam ediyor|halen|devam ediyor|günümüz|hâlen|şu anda|şuan|şu an|şimdi|Şu An|Şu anda)', '2020', tarih, flags=re.IGNORECASE)
        tarih = re.sub(r'(devam|Devam)', '2020', tarih, flags=re.IGNORECASE)
        tarih = re.sub(r'(çalışıyor|çalışıyor)', '', tarih, flags=re.IGNORECASE)
        # Ay isimlerini kaldır
        tarih = re.sub(r'(January|February|March|April|May|June|July|August|September|October|November|December|Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)', '', tarih, flags=re.IGNORECASE)
        
        # '01.2025' gibi ifadeleri yalnızca '2025' haline getir
        tarih = re.sub(r'\b\d{2}\.(\d{4})\b', r'\1', tarih)
        tarih = re.sub(r'\b(\d{2})\/(\d{4})\b', r'\2', tarih)  # '12/2014' gibi tarihleri sadece yıl haline getir
        tarih = re.sub(r'\bıs\s*(\d{4})\b', r'\1', tarih)  # 'ıs' ile ayrılan tarihleri yıl haline getir

        tarih = re.sub(r' ', '', tarih, flags=re.IGNORECASE)
        
        # Temizlenmiş tarihi listeye ekle
        temiz_tarih_listesi.append(tarih.strip())
    
    # Temizlenmiş tarihleri tekrar ',' ile birleştir (boşluk bırakmadan)
    return ','.join(temiz_tarih_listesi)

def calisma_zamani_hesapla(value):
    # Eğer boş veya eksik bir değer varsa
    if not value or pd.isna(value):
        return 0

    # Veriyi virgülle ayır ve her bir tarihi işle
    tarih_listesi = str(value).split(',')
    tarih_araliklari = []

    # Tarih çiftlerini ayır ve listeye ekle
    for tarih_cifti in tarih_listesi:
        tarih_cifti = tarih_cifti.strip()
        tarihler = tarih_cifti.split('-')
        if len(tarihler) == 2:
            try:
                baslangic = int(tarihler[0].strip())
                bitis = int(tarihler[1].strip())
                tarih_araliklari.append((baslangic, bitis))
            except ValueError:
                continue  # Geçersiz tarih çiftlerini atla

    # Eğer liste boşsa sıfır döndür
    if not tarih_araliklari:
        return 0

    # Tarih aralıklarını başlangıca göre sıralıyoruz
    tarih_araliklari.sort()

    toplam_calisma_zamani = 0
    en_erken_baslangic = tarih_araliklari[0][0]  # İlk çalışmaya başlama yılı
    en_son_bitis = tarih_araliklari[0][1]       # İlk işin bitiş yılı

    for baslangic, bitis in tarih_araliklari[1:]:
        if baslangic > en_son_bitis + 1:
            # Boşluk varsa önceki süreyi ekle ve aralığı sıfırla
            toplam_calisma_zamani += (en_son_bitis - en_erken_baslangic + 1)
            en_erken_baslangic = baslangic
            en_son_bitis = bitis
        else:
            # Kesintisiz çalışma durumunda son bitişi güncelle
            en_son_bitis = max(en_son_bitis, bitis)

    # Son kalan aralığı ekle
    toplam_calisma_zamani += (en_son_bitis - en_erken_baslangic + 1)

    return toplam_calisma_zamani


def kontrol_ve_guncelle_ozel(df):
    # Sadece istenilen başlıklar için işlem yap
    columns_to_check = [
        'ÖNE ÇIKAN PROJE', 
        'İÇERİK', 
        'GÖNÜLLÜLÜK YAPTIĞI ORGANİZASYON ADI', 
        'GÖNÜLLÜLÜK ROLÜ', 
        'GÖNÜLLÜ PROJE/YAPILAN İŞ',
        'SERTİFİKA ADI'
    ]
    
    for column in columns_to_check:
        if column in df.columns:
            # Her sütunda 'Belirtilmemiş' veya boş veri varsa 0, diğer durumlarda 1 atanır
            df[column] = df[column].apply(lambda x: 0 if pd.isna(x) or x == 'Belirtilmemiş' or not x else 1)
    
    return df
bolum_eslesme={
  "bilgisayar bilimi": [
    "veritabanları",
    "intranetworking engineering","systems analysis and design",
    'bilgisayar bilimleri',"simulation and game programming",
    "bilgisayar bilimi",
    "computer science",
    "bilgisayar mühendisliği",
    "computer engineering",
    "bilgisayar mühendisliği ve teknoloji",
    "computer science and engineering",
    "computer science and information systems",
    "computer studies",
    'bilgisayar_teknolojileri',
    'bilgisayar_bilimi',
    'bilgisayar bilimleri ve i̇şletme yönetimi',
    'bilgisayar bilimleri ve mühendislik',
    'bilgisayar bilimleri',
    'bilgisayar ağları ve siber güvenlik'
    'bilgisayar ağı',
    'bilgisayar ve i̇şletme bilimleri',
    'bilgisayar programlama teknolojisi',
    'bilgisayar bilgi sistemleri',
    'bilgisayar mühendisliği ve teknolojisi',
    'bilgisayar bilimi ve mühendislik',
    'bilgisayar programcılığı',
    'bilgisayar yönetimi ve bilgi sistemleri',
    'elektrik ve bilgisayar mühendisliği',
    'bilgisayar ve bilgi teknolojileri',
    'bilgisayar ağ teknolojisi',
    'uygulamalı bilgisayar bilimi',
    'bilgisayar bilimleri ve teknolojisi',
    'bilgisayar bilimleri',
    'bilgisayar bilimleri ve saf matematik',
    'bilgisayar uygulaması',
    'bilgisayar bilimi ve bilişim teknolojileri',
    'bilgisayar bilimi ve teknolojisi',
    'bilgisayar bilimibilgisayar bilimi ve teknolojisi',
    'bilgisayar bilimi ve uygulamaları',
    'bilgisayar bilimleri',
    'bilgisayar bilimleri ve teknolojileri',
    'bilgisayar bilimleri ve mühendisliği',
    'bilgisayar ağı uzmanı',
    'bilgisayar sistemleri ağı',
    'yazılım mühendisliği ve bilgisayar bilimleri',
    'bilgisayar_bilimi',
    'bilgisayar_teknolojileri',
    'bilgisayar bilimleri',
    'matematik ve bilgisayar bilimleri',
    'bilgisayar ağları ve siber güvenlik',
    'bilgisayar ağı',
    'ulusal savunma/biyoloji/bilgisayar bilimleri',
    'bilgisayar bilimleri/i̇lgili alan',
    'bilgisayar bilimleri mühendisliği',
    "bilgisayar teknolojileri",
    "computer technologies",
    "bilgisayar uygulamaları",
    "computer applications",
    "computer technology",
    'bilgisayar bilimleri',
    "computer integrated manufacturing and management",
    "computer application",
    "computer information systems",
    "industrial technology interactive computer graphics 3d",
    "engineering computer science",
    "computer science and information systelisans",
    "applied and computational mathematics",
    "computer data processing",
    "computer information system",
    "computer network engineering",
    "computer engineering technology",
    "computer network & security",
    "computer science engineering",
    "master of computer science",
    "computer programming and database development",
    "computer systems",
    "computer networking and security technology belirtilmemiş cisco",
    "computer science & engineering",
    "computers information systems",
    "master of computer applications",
    "yazılım_geliştirme",
    "agile yazılım geliştirme",
    "yazılım mühendisliği",
    "yazılım geliştirme sertifikası",
    "yazılım mühendisliği ve bilgisayar bilimleri",
    "yazılım geliştirme","computer networking and security technology - cisco",
    "software development",
    "software engineering","teknoloji",
    "bilgisayar bilimleri / bilgi sistemleri",
    "computer networking and security technology belirtilmemiş cisco","bilgisayar bilimleri", "computer science", "bilgisayar mühendisliği", 
    "computer engineering", "yazılım mühendisliği", "software engineering", 
    "bilgi teknolojileri", "information technology", "data science", "cyber security", 
    "information systems", "networking", "computer applications", 
    "information technology systems", "information assurance and cybersecurity","bilgisayar bilimi",
        "artificial intelligence and machine learning",
        "computer networking and security technology belirtilmemiş cisco","bilgisayar bilimi",
        "computer networking and security technology belirtilmemiş cisco",
  ],
  "işletme ve yönetim": [
      "yönetim ve üretim","pazarlama/i̇şletme yönetimi","stratejik yönetim","supply chain operations","i̇şletme ve bilim",
        "tedarik zinciri yönetimi","i̇şletme yönetimi ve teknolojisi",
        "işletme","bachelor of business administration","kurumsal sekreterlik", "business administration", "işletme yönetimi", "business management", 
        "business", "management", "i̇şletme yönetimi ve insan kaynakları", 
        "business administration in project management", "işletme ve bilim", 
        "business administration & management","işletme","business administration","işletme yönetimi","business management","business", "management","i̇şletme",
        "business administration in accounting","girişimcilik","business & entrepreneurship",
        "management in finance","i̇şletme yönetimi - pazarlama",
        "i̇ş analitiği","i̇şletme yönetimi – operasyon yönetimi",
        "leadership and management",
        "işletme yönetimi","ekonomi ve yönetim",
        "uluslararası i̇şletme","mba hr",
        "i̇şletme ve yönetim",
        "business marketing",
        "business administration: management",
        "business analytics & economics","işletme ve yönetim",
        "i̇şletme yönetimi",
        "master of business administration",
        "mba",
        "business management / finance",
        "mba in management",
        "i̇şletme analitiği",
        "liderlik ve yönetim",
    ],
    "elektrik mühendisliği": [
        "elektronik ve enstrümantasyon mühendisliği","elektronik ve haberleşme","electronic engineering technology",
    "elektrik mühendisliği","elktronik ve haberleşme",
    "electrical engineering",
    "elektrik ve elektronik mühendisliği",
    "electrical and electronics engineering",
    "electronics and computers","elektrik mühendisliği",
        "electronics and communications",
        "elektronik ve haberleşme mühendisliği", "elektrik_mühendisliği",
        "electronics and communication engineering",
        "electronics & instrumentation engineering",
        "elektronik mühendisliği","elektrik ve endüstriyel elektronik","elektronik ve telekomünikasyon mühendisliği"
  ],
  "makine mühendisliği": [
    "makine mühendisliği",
    "mechanical engineering",
    "makine mühendisliği ve teknoloji","makine mühendisliği",
        "mechanical engineering",
        "structural engineering",
  ],
  "endüstri mühendisliği": [
    "endüstri mühendisliği",
    "industrial engineering",
    "endüstriyel mühendislik",
    "endüstri mühendisliği",
        "production engineering",
  ],
  "sağlık bilimleri": [
        "sağlık bilimleri", "healthcare informatics","health sciences", "bio medical engineering", 
        "healthcare administration", "public health officer", "health information technology", 
        "geriatrik hizmetler", "geriatrics","sağlık bilimleri","health sciences","health and medical sciences","sağlık bilimleri",
        "healthcare management","veterinerlik ön lisansı",
        "public health nursing","pre-pharmacy studies",
        "nursing","behavioral health","s.s.c.",
        "tıp ve psikiyatri sosyal hizmetler",
        "sağlık yönetimi","pre-medicine",
        "sağlık bilimleri",
        "sağlık yönetim sistemleri",
        "global and community health",
        "public health nursing",
        "sağlık bilişimi",
        "clinical mental health counseling",
    ],
  "veri bilimi": [
    "veri bilimi","veri tabanı yönetim sistemleri",
    "data science","yönetim ve bilişim",
    "data analytics", "veri bilimi","veri tabanları",
        "data science",
        "veri analitiği",
        "veri tabanı yönetimi","veri_bilimi",
        "data science",
        "veri tabanı teknolojisi",
        "veri analizi",
  ],
  "bilgi teknolojileri": [
    "veri modelleme ve veritabanı yönetimi","cyber security management and policy","yönetim sertifikası","siber güvenlik mühendisliği","bt proje yönetimi","teknoloji yönetimi","database design",
    "bilgi sistemleri","full stack web development",
    "information systems","broadcast technology",
    "information technology","process technology",
    "information technology systems","siber güvenlik ve adli bilimler",
    "information systems and cyber security","dniit programı",
    "information assurance and cybersecurity",
    "management information system","network and system administration",
    "information system management",
    "information technology and management",
    "business information technology",
    "information systems engineering",
    "information and communication sciences",
    "information science",
    "information systems engineering and management",
    "computer information systems",
    "computer science and information systems",
    "information systems & e-commerce",
    "information systems and cyber security",
    "information systems and technology",
    "management of information systems",
    "information systems and decision making",
    "management information systems & marketing",
    "data science and information systems",
    "information technology in management",
    "business administration in information systems",
    "information systems & business systems",
    "information technology and systems",
    "bilgi sistemleri",
    "bilgi sistemleri yönetimi",
    "bilgi teknolojileri",
    "bilgi sistemleri ve siber güvenlik",
    "bilgi bilimi ve teknolojisi",
    "bilgi sistemleri mühendisliği ve yönetimi",
    "bilgi bilimleri ve teknolojisi",
    "bilgi teknolojisi ve sistem mühendisliği",
    "bilgi ve karar bilimleri",
    "bilgi teknolojisi ve sistem yönetimi",
    "bilgi bilimi",
    "bilgi ve karar bilimleri",
    "bilgi sistemleri / veritabanı yönetimi",
    "bilgi sistemleri ve yönetimi",
    "bilgi teknolojileri ve yönetimi",
    "yönetim belirtilmemiş bilgi sistemleri",
    "bilgi_sistemleri",
    "bilgi sistemleri","database technologies",
    "i̇şletme bilgi sistemleri",
    "bilgi teknolojisi",
    "kütüphane ve bilgi bilimi",
    "i̇şletme yönetimi ve bilgi sistemleri",
    "i̇şletme bilgi sistemleri yönetimi",
    "i̇şletme bilgi teknolojisi",
    "tedarik zinciri yönetimi ve bilgi teknolojileri ve sistemleri",
    "sağlık bilgi teknolojisi ve yönetimi",
    "coğrafi bilgi sistemleri",
    "yönetim bilgi sistemleri",
    "i̇leri bilgi sistemleri",
    "coğrafi bilgi sistemleri ve uzaktan algılama",
    "yönetim ve bilgi sistemleri",
    "bilgi teknolojisi ve siber güvenlik",
    "yönetim bilgi sistemi"
    "information technology/business systems",
    "business management & information technology",
    "information system",
    "business administration in information and supply chain management",
    "computer science and information systelisans",
    "information quality",
    "health information technology",
    "information systems",
    "computer information system"
    "management information science",
    "geographic information systems",
    "management information systems",
    "archaeological information systems",
    "management and information systems",
    "computing & information",
    "business administration and management information systems",
    "information assurance",
    "computers information systems",
    "yönetim belirtilmemiş bilgi sistemleri",
    "yönetim bilgi sistemi",
    "information technology/business systems",
    "risk management/information systems",
    "management information science","bilgi teknolojileri",
        "cybersecurity",
        "network and communications management",
        "ağ merkezli bilişim",
        "electronics and communication; vlsi & system programming", "bilgi teknolojileri",
        "ağ merkezli bilişim",
        "bt operasyonları",
        "cyber security engineering","yönetim - bilgi sistemleri","bilgi teknolojileri","networking services technology",
    ],
    "sosyal bilimler": [
        "i̇ngilizce ve felsefe","terörizm/çounter terörizm","yaratıcı yazarlık","kriminoloji","social science","criminal justice","history and classical languages",
        "sosyoloji", "sociology", "psikoloji", "psychology", "felsefe", 
        "philosophy", "edebiyat", "literature", "history", "international law", 
        "sociology in spanish", "public relations", "linguistics", "cultural anthropology",
        "psikoloji","cosmetology","counseling psychology","din ve i̇nsani yardım",
        "psychology","geography","uygulamalı jeofizik","dil ve yazı",
        "coğrafya ve kırsal kalkınma","vokal müzik ve genel i̇şletme",
        "law","felsefe - pre-law","religious ethics",
        "international law","i̇nsan hizmetleri",
        "pre-law","sosyal bilimler","yaşam bilimleri",
        "psychology clinical","antropoloji","i̇k ve pazarlama",
        "human resource management","halkla i̇lişkiler ve dijital fotoğrafçılık",
        "uluslararası çalışmalar ve politika","sosyal bilimler","planlama ve politika sosyal hizmetler",
        "siyaset bilimi","ceza adaleti ve psikoloji","kamu politikası",
        "sosyal ve kültürel antropoloji","siyasi bilimler","tarih","sosyal hizmet",
    ],"fen bilimleri": [
        "plant physiology","matematik ve fizik",
        "associates of science","bilim","gifted science program","medical","fizik ve elektronik",
        "i̇statistik","marine biology",
        "master's in science","matematik", "mathematics", "applied mathematics", "mathematics and physics", 
        "kimya", "chemistry", "fizik", "physics", "biyoloji", "biology", "biological sciences","fizik",
        "physics","matematik","aktüerya bilimi",
        "mathematics","science",
        "applied mathematics",
        "computing",
        "mobile and ubiquitous computing","kimya",
        "chemistry",
        "kimya mühendisliği",
        "chemical engineering","fen bilimleri",
        "biochemistry",
        "molecular biology",
        "uygulamalı bilimler","fen bilimleri",
        "biyolojikimya","uygulamalı matematik",
        "general science",
        "doğa bilimleri","general/business/science courses",
    ],
    "sanat ve tasarım": [
        "ux research and design",
        "görsel sanatlar", "visual arts", "sanat", "art", "grafik tasarım", 
        "graphic design", "müzik", "music", "tasarım", "design", "film/video", 
        "creative writing", "sanat ve tasarım",
        "grafik tasarım / reklamcılık",
        "fine arts",
        "liberal arts in science and culture", "sanat ve tasarım",
        "grafik tasarım asistanlığı",
        "sanat çalışmaları",
    ],
    "ekonomi ve finans": [
        "yönetim ve finans","pazarlama ve i̇hracat","mali muhasebe",
        "economics minor","financial services","yönetim ve kamu politikası","muhasebe ve finans","ekonomi ve matematik",
        "business intelligence","business and medical office",
        "proje yönetimi","operasyon yönetimi","i̇nsan kaynakları ve sağlık yönetimi","i̇şletme yönetimi ve i̇nsan kaynakları","muhasebe sertifikası",
        "ticaret","marketing management","marketing","gerontology",
        "muhasebe","yönetim","pazarlama","organizasyonel liderlik",
        "economics", "finance", "business analytics", "financial management", "banking and finance", 
        "accounting","ekonomi","ekonomi ve girişimcilik gelişimi",
        "finans","muhasebe sertifikası","accounting and finance",
        "bankacılık ve finans","ev ekonomisi",
        "financial mathematics & statistics",
        "accounting & management studies", "ekonomi ve finans",
        "banking & finance",
        "financial accounting","işletme ve yönetim",
        "işletme ve yönetim","i̇nsan kaynakları yönetimi",
        "yönetim bilişim sistemleri",

    ],
    "mühendislik":[
        "applied sciences and engineering","elektronik ve i̇letişim mühendisliği","metalurji mühendisliği","i̇nşaat mühendisliği","sistem mühendisliği","aeronautical engineering","modeling and simulation engineering",

    ],
    "uluslararası çalışmalar ve politika": [
        "uluslararası i̇ş uygulamaları","uluslararası çalışmalar","afrika çalışmaları",
        "uluslararası ticaret","international studies", "international relations", "political science", 
        "political science & business", "international law and diplomacy", "global entrepreneurship","uluslararası i̇şletme yönetimi",
        "b.sc. political science and public administration",
        "international relations and strategic studies","uluslararası çalışmalar ve politika",
        "international politics","uluslararası çalışmalar ve politika",
    ],
    "teknik bilimler": [
        "school of professional and graduate studies/technical courses",
        "engineering","teknik lingkungan","mekanik",
        "mühendislik teknolojisi","alet tasarımı ve bakımı"
        "elektronik ve matematik","genel çalışmalar",
    ],
    "eğitim bilimleri": [
        "teknoloji ve erken çocukluk eğitimi","diploma","self-determined studies","english","entrepreneurial studies","fransızca","i̇spanyolca","bachelor's","european languages",
        "research","general studies","dilbilim",
        "early childhood development in education",
        "eğitim bilimleri","eğitim","i̇ngilizce",
        "english education","outdoor education","transformative inquiry & consciousness studies",
    ],
    "hukuk": [
        "özel uluslararası hukuk","paralegal studies",
        "çocuk ve aile hukuku","justice administration",
        "adalet sistemi","hukuk","criminology",
        "çocuk ve aile hukuku","uluslararası hukuk ve diplomasi"
        "legal studies","suç bilimi",
    ],
    "iletişim": [
        "kitle i̇letişimi ve yayıncılık","human relations",
        "radio announcing and advertising",
        "elektronik ve i̇letişim","telekomünikasyon",
        "business communications","journalism/public relations",
        "i̇letişim çalışmaları",
        "mass communication","kitle i̇letişimi",
        "gazetecilik",  "iletişim","̇letişim",
        "gazetecilik",
        "mass communication",
        "halkla i̇lişkiler",
    ],
    "sanat ve kültür": [
        "kültür ve sanat","dans","amerikan kültürü ve müzik",
        "african studies","b arts","film ve video","film",
        "english literature","liberal arts","sanat ve tasarım",
    ],
    "çevre mühendisliği": [
        "environmental & resource engineering","rekreasyon çalışmaları","environmental geography","agriculture",
        "environmental planning","çevre çalışmaları",
        "environmental geography","park ve rekreasyon yönetimi",
        "civil and environmental engineering"
    ]

}

kurulus_eslesme={'aws': ['amazon web services',
  'aws',
  'amazon web hizmetleri',
  'amazon web servisi',
  'amazon',
  'amazon web hizmetleri (aws)',
  'amazon web service'],
 'scrum alliance': ['scrum alliance',
  'scrum i̇ttifakı',
  'scrum.org',
  'international scrum institute',
  'uluslararası scrum enstitüsü',
  'scrum institute',
  'scrum study',
  'scrum'],
 'oracle': ['oracle', 'oracle corporation', '[oca certifying organization]'],
 'microsoft': ['microsoft',
  'microsoft corporation',
  'microsoft sertifikalı sistem mühendisi'],
 'comptia': ['comptia'],
 'project management institute': ['project management institute', 'pmi'],
 'istqb': ['istqb', 'astqb'],
 'itil': ['itil',
  'itil foundation',
  'itil temel seviye',
  'itil organizasyonu'],
 'tableau': ['tableau', 'tableau training academy'],
 'cisco': ['cisco',
  'cisco meraki',
  'cisco networking academy',
  'cisco sertifikalı ağ ortağı'],
 'vmware': ['vmware'],
 'red hat': ['red hat'],
 'google': ['google', 'google afrika'],
 'ibm': ['ibm'],
 'salesforce': ['salesforce'],
 'sap': ['sap'],
 'udemy': ['udemy'],
 'ec-council': ['ec-council'],
 'edureka': ['edureka.co'],
 'apics': ['apics'],
 'six sigma': ['six sigma', 'six sigma institute', 'lssgb'],
 'acca': ['acca', 'acca uk'],
 'exin': ['exin'],
 'sun microsystems': ['sun microsystems', 'sun yetkili eğitim merkezi'],
 'goethe institute': ['goethe enstitüsü', 'max mueller bhavan'],
 'coursera': ['coursera',
  'coursera/duke university',
  'edx & university of adelaide'],
 'servicenow': ['servicenow'],
 'pivotal': ['pivotal'],
 'docker': ['docker inc.'],
 'cloudera': ['cloudera','cloud u'],
 'hortonworks': ['hortonworks'],
 'epic': ['epic', 'epic'],
 'infosys': ['infosys'],
 'toastmasters': ['toastmasters uluslararası'],
 'nutanix': ['nutanix'],
 'blackbaud': ['blackbaud'],
 'rational rose': ['rational rose'],
 'splunk': ['splunk'],
 'mariadb': ['mariadb'],
 'postgresql': ['postgresql'],
 'enterprisedb': ['enterprisedb'],
 'sas': ['sas'],
 'data group usa': ['data group usa'],
 'indeed assessments': ['indeed assessments'],
 'pega': ['pega sistemleri'],
 'nse': ['nse'],
 'axelos': ['axelos'],
 'mulesoft': ['mulesoft'],
 'kepner tregoe': ['kepner tregoe'],
 'niit': ['niit', 'niit uniqua'],
 'good agile pvt. ltd.': ['good agile pvt. ltd.'],
 'techmahindra': ['techmahindra'],
 'bsi': ['bsi'],
 'cms': ['cms'],
 'luzerne county community college': ['luzerne county community college'],
 'chattahoochee technical college': ['chattahoochee technical college'],
 'mta': ['mta'],
 'data science professional certificate': ['data science professional certificate'],
 'johns hopkins university': ['johns hopkins university'],
 'makerere university': ['makerere üniversitesi'],
 'advance technology solutions': ['advance technology solutions']
}

dil_eslesme={
'ingilizce':['ingilizce','english','i̇ngilzice'],
'çince':['çince','basic chinese','geleneksel çince'],
'belirtilmemiş':['belitilememiş','-'],
'ispanyolca':['ispanyolca','spanish'],
'ispanyolca,ingilizce':['i̇spanyolca / i̇ngilizce'],
'fransızca':['kannada']
}
# 'VEREN KURULUŞ' sütunundaki kuruluşları düzeltme
def duzenle_kurulus(kurulus_adı):
    kurulus_adı = str(kurulus_adı).strip().lower()  # Küçük harfe çevir ve baştaki/sondaki boşlukları kaldır
    kurulus_adı = re.sub(r'\(.*?\)|\(.*', '', kurulus_adı).strip()  # Parantez içi açıklamaları temizle

    # Eğer kurulus_adı NaN (yani boş veya eksik) ise, "Belirtilmemiş" döndür
    if pd.isna(kurulus_adı) or kurulus_adı == ""or kurulus_adı=='-':
        return "belirtilmemiş"
    
    # Virgüllerine ayırarak işlem yapıyoruz
    kurulus_adı_listesi = kurulus_adı.split(',')

    
    
    # Her bir kuruluş adı üzerinde işlem yapıyoruz
    duzeltilmis_kuruluslar = []
    for kurulus in kurulus_adı_listesi:
        kurulus = kurulus.strip().lower()  # Her bir öğeyi küçük harfe çevir ve boşlukları temizle
        # Eşleştirme sözlüğünü kullanarak her kuruluşu düzeltiyoruz
        for standart_kurulus, eslesmeler in kurulus_eslesme.items():
            # Küçük harf farkını gözetmeden eşleşme yap
            if kurulus in (match.lower().strip() for match in eslesmeler):
                duzeltilmis_kuruluslar.append(standart_kurulus)
                break
        else:
            kurulus=kurulus.replace('-','belirtilmemiş')

            # Eğer eşleşme yoksa, orijinal ismi ekle
            duzeltilmis_kuruluslar.append(kurulus)
    
    # Düzeltilmiş kuruluşları tekrar virgülle birleştiriyoruz
    return ','.join(duzeltilmis_kuruluslar)



# 'BÖLÜM ADI' sütunundaki bölümleri düzeltme
def duzenle_bolum(bolum_adı):
    bolum_adı = str(bolum_adı).strip().lower()  # Küçük harfe çevir ve baştaki/sondaki boşlukları kaldır
    bolum_adı = re.sub(r'\(.*?\)|\(.*', '', bolum_adı).strip()  # Parantez içi açıklamaları temizle

    # Eğer bolum_adı NaN (yani boş veya eksik) ise, "Belirtilmemiş" döndür
    if pd.isna(bolum_adı) or bolum_adı == "":
        return "belirtilmemiş"
    
    # Virgüllerine ayırarak işlem yapıyoruz
    bolum_adı_listesi = bolum_adı.split(',')

    
    
    # Her bir kuruluş adı üzerinde işlem yapıyoruz
    duzeltilmis_bolumlar = []
    for bolum in bolum_adı_listesi:
        bolum = bolum.strip().lower()  # Her bir öğeyi küçük harfe çevir ve boşlukları temizle
        # Eşleştirme sözlüğünü kullanarak her kuruluşu düzeltiyoruz
        for standart_bolum, eslesmeler in bolum_eslesme.items():
            # Küçük harf farkını gözetmeden eşleşme yap
            if bolum in (match.lower().strip() for match in eslesmeler):
                duzeltilmis_bolumlar.append(standart_bolum)
                break
        else:

            # Eğer eşleşme yoksa, orijinal ismi ekle
            duzeltilmis_bolumlar.append(bolum)
    
    # Düzeltilmiş kuruluşları tekrar virgülle birleştiriyoruz
    return ','.join(duzeltilmis_bolumlar)

pozisyon_eslesme={
        "Bilgisayar Mühendisi": ["Bilgisayar Mühendisi", "Bilgisayar mühendisi", "Bilgisayar Bilimleri"],
    "Yazılım Mühendisi": [
        "Yazılım Mühendisi", "Yazılım mühendisi", "BT Yazılım Geliştirme mühendisi", 
        "Kıdemli Yazılım Mühendisi", "Kıdemli Yazılım Geliştiricisi", 
        "Yazılım Geliştiricisi", "YAZILIM GELİŞTİRİCİSİ", "Yazılım geliştirici", 
        "Kıdemli Yazılım Geliştirme Mühendisi", "Baş Yazılım Geliştiricisi", 
        "Yazılım Geliştirme Mühendisi", "Yazılım Mimarı", "Yazılım Mühendisliği", 
        "Yazılım Teknik Destek Mühendisi", "Yazılım Geliştirme mühendisi", 
        "Kıdemli Yazılım Test Mühendisi", "Uzman Yazılım Test Mühendisi", 
        "Kıdemli Yazılım Test Otomasyon Mühendisi", "Yazılım Test Mühendisi", 
        "Baş Personel Yazılım Mühendisi", "Baş Yazılım Geliştiricisi"
    ],
    "Mobil Geliştirici": [
        "Mobil Geliştirici", "Android Geliştirici", "ANDROID geliştirici", 
        "Android Yazılım Geliştirici", "iOS Geliştiricisi", "Kıdemli Android Geliştirici", 
        "Kıdemli iOS Geliştirici", "Mobil uygulama geliştirici", "React Native Mobil Mühendisi", 
        "Kıdemli Android Mühendisi", "Kıdemli iOS Mühendisi", "Baş iOS Geliştiricisi", 
        "Slack Uygulama Geliştiricisi", "Kıdemli Unity Yazılım Mühendisi", 
        "mobil oyun geliştirici", "RoR Fullstack Mühendisi"
    ],
    "Full Stack Geliştirici": [
        "Full Stack Yazılım Mühendisi", "full stack geliştirici", 
        "Full-Stack Ürün Mühendisi", "Full stack Angular Java geliştiricisi", 
        "Platform Mühendisi", "Platform Yazılım Mühendisi"
    ],
    "DevOps Mühendisi": [
        "DevOps mühendisi", "Kıdemli DevOps Mühendisi", "Azure DataOps Mühendisi", 
        "Veri DevOps Mühendisi", "Orta DevOps mühendisi", "Bulut ve DevOps Danışmanı"
    ],
    "Java Geliştirici": [
        "Java Geliştiricisi", "java geliştiricisi", "Java Yazılım Mühendisi", 
        "Full stack Angular Java geliştiricisi", "Lider Java Geliştiricisi", 
        "Java AI Lider Mühendisi"
    ],
    "Frontend Geliştirici": [
        "Frontend Geliştiricisi", "Frontend Geliştirici", "Kıdemli Frontend Yazılım Mühendisi"
    ],
    "Backend Geliştirici": [
        "Backend yazılım Mühendisi", "JavaScript Geliştiricisi", ".NET Geliştiricisi", 
        "PHP Geliştiricisi"
    ],"Yazılım Geliştirme ve Mühendislik": [
        "Web Developer", "Cyber Security Analyst / RMF Specialist", "Yazılım Geliştirici (Software Engineer)"
    ],
    "Finans ve Muhasebe": [
        "Financial Analyst", "Accounting Assistant", "Assistant Accountant"
    ],
    "Eğitim ve Danışmanlık": [
        "Substitute Teacher"
    ],
    "Müşteri ve Kalite Destek": [
        "Customer Quality Specialist"
    ],
    "Veritabanı ve Sistem Yönetimi": [
        "Database Manager"
    ],
    "Veri Analizi ve Araştırma": [
        "Research Analyst", "Public Records Researcher", "Research Technician"
    ],
    "İşletme ve Yönetim": [
        "Operations Analyst", "Business Developer", "Manager & Bartender", "Owner", "Leasing Administrator", 
        "Contractor", "Case Manager", "Social Media Specialist", "Sales Administrator", "Sales/Merchandising Assistant", 
        "Specialist Sales Associate"
    ],
    "Lojistik ve Operasyon": [
        "Field Operations Supervisor", "Logistics Analyst", "Warehouse Database Manager", "Warehouse Specialist", 
        "Warehouse Employee", "Fleet Manager/Administrator", "Service Operations Associate", "Logistics Coordinator"
    ],
    "Müşteri Hizmetleri ve Perakende": [
        "Customer Service Agent", "Electronics Customer Service Representative", "Receptionist for Admissions Department", 
        "Sales Assistant", "Store Manager", "Sales/Merchandising Assistant"
    ],
    "Gönüllü ve Topluluk Hizmeti": [
        "Volunteer", "Volunteer Coordinator", "Volunteer Resource Center", "Summer Missionary"
    ],
    "Fotoğrafçılık ve Medya": [
        "Photographer/Film Editor", "Cameraman", "Event Coordinator", "Graphic Designer/Website Editor"
    ],
    "Teknik Destek ve Operasyon": [
        "Remote Helpdesk Technician", "Audio Video Administrator", "Cable Technician", "Remote Hands Technician", 
        "Tracking Agent/Database Administrator", "Technical Business Analyst"
    ],
    "İleri Seviye İdari Pozisyonlar": [
        "Executive Assistant", "Manager & Bartender", "Store Manager", "Müdür/Kasiyer", "Officer", 
        "Sales Administrator", "Constituent Affairs Intern", "Legal Secretary", "Litigation Assistant"
    ],
    "Mutfak ve Konuk Hizmetleri": [
        "Cook", "Kitchen Helper", "Host", "Hostess/Server Assistant/Prep Cook", "Lead Galley Steward"
    ],
    "Güvenlik ve Bakım": [
        "Security Guard/Firefighter", "Surgical Attendant", "Asset Protection Supervisor", 
        "Tactical Power Generation Specialist"
    ],
    "Sağlık ve Bakım": [
        "Massage Therapist", "Voluntary Massage Therapist", "Yoga Therapist", "Child Care Staff"
    ],
    "Taşımacılık ve Dağıtım": [
        "Driver", "Rural Carrier Associate", "Package Handler", "Warehouse Database Manager"
    ],
    "Perakende ve Toptan Satış": [
        "Retail Sales Representative", "Retail Sales Consultant", "Specialist Sales Associate"
    ],
    "Yazılım ve Dijital Çözümler": [
        "AWS Engineer", "Salesforce Administrator Consultant", "Salesforce Administrator", "Business Application Developer"
    ],
    "İleri Seviye Destek ve İdari Görevler": [
        "Administrative Assistant II", "Operations Analyst", "Accounting Assistant II", "Accounting Assistant"
    ],
    "Sanat ve Yaratıcılık": [
        "Science Fiction Writer", "Photographer/Film Editor"
    ],
    "Müşteri İlişkileri ve İletişim": [
        "Client Intake/Scheduler", "Customer Service Representative", "Sales Coordinator"
    ],
    "Gömülü Sistem Mühendisi": [
        "Gömülü Yazılım Tasarım Mühendisi", "Kıdemli Gömülü Yazılım Mühendisi", 
        "Gömülü Linux Yazılım Mühendisi", "Gömülü Linux Danışmanı", 
        "Kıdemli Gömülü Linux Yazılım Mühendisi"
    ],
    "Makine Öğrenmesi ve AI Mühendisi": [
        "Makine Öğrenmesi Mühendisi", "Kıdemli Makine Öğrenme Mühendisi", 
        "Baş Makine Öğrenme Mühendisi", "Derin Öğrenme Mühendisi", 
        "Java AI Lider Mühendisi"
    ],
    "Veri Mühendisi": [
        "Veri Mühendisi", "Veri Yazılım Mühendisi"
    ],
    "Sistem Mühendisi": [
        "Sistem Mühendisi", "Sistem Geliştirici", "Kıdemli Sistem Mühendisi", 
        "Kıdemli Yazılım Geliştirme Mühendisi", "VMware Uzmanı"
    ],
    "Bulut Mühendisi": [
        "Bulut Yazılım Geliştiricisi", "Bulut ve DevOps Danışmanı", 
        "Bulut Mühendisi", "Kıdemli Personel Bulut Mühendisi"
    ],
    "Veritabanı Yöneticisi ve Geliştirici": [
        "Veritabanı Yöneticisi (Database Administrator / DBA)",
        "Oracle Veritabanı Yöneticisi / Oracle DBA",
        "SQL Veritabanı Yöneticisi / SQL DBA",
        "PostgreSQL Veritabanı Yöneticisi",
        "Microsoft SQL Server Veritabanı Yöneticisi",
        "Veritabanı Yöneticisi / Geliştirici",
        "Kıdemli Veritabanı Yöneticisi (Sr. Database Administrator)",
        "Junior Veritabanı Yöneticisi (Junior DBA)",
        "SQL Veritabanı Geliştiricisi",
        "SQL Server Veritabanı Uzmanı / DBA",
        "Data Modeler / DBA",
        "Production Support Database Administrator",
        "Database Admin / Developer",
        "Application Database Administrator",
        "Oracle Database Administrator Clusterware and ASM",
        "Database Development Engineer",
        "Oracle Junior DBA",
        "Junior SQL Server Database Administrator",
        "SQL Developer / DBA",
        "SQL Database Analyst",
        "Lead Oracle DBA",
        "Database Administrator / SQL Developer",
        "DevOps DBA",
        "Principal Database Development Engineer"
    ],
    "Veritabanı Analisti ve Veri Yönetimi": [
        "Veritabanı Analisti (Database Analyst)",
        "SQL Database Analyst",
        "Business Intelligence Veritabanı Yöneticisi",
        "Data Engineer",
        "Veritabanı ve Sistem Danışmanı",
        "Research Database Administrator",
        "Sr. Database Analyst / Project Manager",
        "Veritabanı ve Güvenlik Yöneticisi",
        "Sr. MongoDB Architect / Administrator",
        "Development Database Manager"
    ],
    "Teknik Destek ve Sistem Yönetimi": [
        "Teknik Destek Uzmanı (Technical Support Specialist)",
        "Sistem Yöneticisi (Systems Administrator)",
        "Systems / Database Administrator",
        "IT Support Administrator",
        "Network and Database Administrator",
        "Application Support Analyst",
        "Systems Developer",
        "IT Manager / Interim IT Manager",
        "Help Desk Manager",
        "IT Technician"
    ],
    "Proje ve Süreç Yönetimi": [
        "Scrum Master",
        "Yardımcı Scrum Master",
        "Proje Yöneticisi (Project Manager)",
        "Agile Business Analyst",
        "Development Operations Manager"
    ],
    "Veri Ambarı ve İş Zekası": [
        "Veri Ambarı Mühendisi",
        "Business Intelligence",
        "Data Warehouse Engineer"
    ],
    "Veritabanı Yöneticisi": [
        "Oracle Database Administrator", "Oracle Database Administrator II", 
        "Oracle Database Administrator I", "Database Administrator MSSQL Server", 
        "SQL Server DBA", "SQL Server DBA II", "SQL Server Veritabanı Yöneticisi", 
        "Operational Support Database Administrator", "Senior Database Administrator", 
        "Junior Database Administrator", "Oracle Veri Tabanı Yöneticisi", 
        "Veritabanı Destek Mühendisi - Stajyer", "Veritabanı Yöneticisi Stajyeri", 
        "Oracle Veritabanı Yöneticisi Stajyeri", "Oracle Product Specialist / Junior DBA", 
        "Oracle Veri Tabanı Yöneticisi", "Sistem Mühendisi ve Veritabanı Yöneticisi", 
        "Database and Application Administrator", "Network Security and Database Administrator", 
        "Senior SQL Server DBA/Engineer", "Database Administrator I/ Sysadmin"
    ],
    "Yazılım Geliştirici": [
        "Creator/Developer", "Software Engineer Intern", "Junior Developer", 
        "Application Developer Intern", "Web Developer/GIS Coordinator", 
        "Programmer Analyst", "Software Developer", "Assistant System Engineer", 
        "Computer System Analyst", "Programmer/CNC", "Network and Database Administrator", 
        "Java Tutor", "Web Development and Database Administrator", 
        "BI Developer", "HealthShare Developer", "Application Development Team Lead", 
        "Developer", "Java Developer", "DevOps Engineer", "Software Eng Intern"
    ],
    "Analist": [
        "Actimize Analyst", "Lead Analyst/Product Owner", "Business Intelligence Analyst Intern", 
        "Data/QA Analyst", "Data/Business Analyst", "Research Assistant", 
        "Health Data Analyst", "SQL- Developer", "Security Operation Center Analyst", 
        "Techno-Functional Consultant", "QA Testing/Business Analyst", 
        "Business Analyst & Consultant", "Data Analyst", "Data Analyst Intern", 
        "Sourcing Specialist", "Data Entry", "Power BI Analyst", 
        "E-commerce Manager / Customer Service Representative"
    ],
    "BT ve Teknik Destek": [
        "BT Asistanı", "IT Support Specialist", "IT Administrator/Database Management Specialist", 
        "Servicenow Trainee Analyst", "Desktop Support Specialist in IT Services", 
        "Help Desk Support", "Scanner Technician", "Private Contractor", "IT Consultant", 
        "IT Intern", "I.T. Support Technician", "IT Support", "General Cleaner", 
        "Hostess/Server Assistant/Prep Cook"
    ],
    "Proje Yönetimi ve Liderlik": [
        "Project Leader", "Team Lead & Social Media Ambassador", 
        "Lead Technology Specialist", "Manager Database Systems", 
        "Lead Member of Group Google Vision API for Receipt OCR", 
        "Lead Analyst/Product Owner", "Team Coordinator/Editor", "Senior Specialist", 
        "Senior Engineer"
    ],
    "Stajyer ve Asistan": [
        "Stajyer", "Veritabanı Yönetimi Öğrencisi", "Makine Öğrenimi Öğrencisi", 
        "Business Intelligence Analyst Intern", "Database Administrator - Intern", 
        "Constituent Affairs Intern", "Sales Coordinator", "Intern"
    ],
    "İnsan Kaynakları ve Yönetim": [
        "Human Resources", "Recruiter", "Human Resources Assistant/Receptionist", 
        "Administrative Assistant", "Administrative Assistant/Database Administrator"
    ],
    "veritabanı yöneticisi": [
        "veritabanı yöneticisi",
        "database administrator",
        "sql database administrator",
        "oracle database administrator",
        "mssql database administrator",
        "mysql database administrator",
        "sr. database administrator",
        "junior database administrator",
        "production database administrator",
        "postgresql database administrator",
        "database and campaign administrator"
    ],
    "veritabanı geliştiricisi": [
        "veritabanı yöneticisi / geliştirici",
        "veritabanı geliştiricisi",
        "database developer",
        "programmer & database administrator",
        "web application programmer & database administrator",
        "database developer / administrator",
        "database lead",
        "developer and database administrator",
        "database developer | administrator"
    ],
    "proje yöneticisi": [
        "proje yöneticisi",
        "project manager",
        "program manager",
        "project lead",
        "sr. project manager",
        "project manager/analyst",
        "proje yöneticisi / iş analisti"
    ],
    "iş analisti": [
        "iş analisti",
        "business analyst",
        "data/business analyst",
        "sr. business analyst/project manager",
        "business systems analyst/test coordinator",
        "junior business analyst/test coordinator"
    ],
    "teknik destek uzmanı": [
        "teknik destek",
        "it support administrator",
        "system administrator",
        "systems/database administrator",
        "desktop support administrator"
    ],
    "yazılım geliştirici": [
        "yazılım geliştirici",
        "software engineer",
        "java developer",
        "full stack developer",
        "backend developer",
        "sr. java j2ee developer/tech lead"
    ],
    "veri analisti": [
        "veri analisti",
        "data analyst",
        "data/business analyst",
        "data/qa analyst",
        "data and information systems coordinator"
    ],
    "müşteri ilişkileri": [
        "müşteri ilişkileri temsilcisi",
        "customer care supervisor",
        "crm coordinator",
        "sales support administrator",
        "customer process önlisans"
    ],
    "geliştirici": [
        "geliştirici",
        "developer",
        "application support analyst",
        "software engineer/database administrator",
        "developer/module lead"
    ],
    "stajyer": [
        "stajyer",
        "intern",
        "junior database administrator",
        "database administrator intern",
        "data analyst intern"
    ],
    "Veritabanı Yöneticisi ve Geliştiricisi": [
        "Oracle ve AWS Veritabanı Yöneticisi", "SQL Server/MS Access Veritabanı Yöneticisi", 
        "Oracle Veritabanı Geliştiricisi/Uygulama Veritabanı Yöneticisi", 
        "SQL Server DBA", "SQL Server Veri Tabanı Yöneticisi", "Oracle SQL Veritabanı Yöneticisi", 
        "Oracle Üretim Destek Veritabanı Yöneticisi", "Applications Database Administrator", 
        "Database Administrator/Digital Data Specialist", 
        "Production SQL Server Database Administrator", "Oracle Database Engineer", 
        "Oracle Core DBA /Production Support Database Administrator", 
        "Sr. SQL Server DBA", "Sr. Oracle Database Administrator", "Sr. Oracle DBA", 
        "Cassandra Admin", "MS SQL Admin", "Cosmos DB Admin", 
        "Jr. SQL Server Database Administrator/Engineer", "Database Development", 
        "Database Administrator III", "SQL Database Administrator - DBA", 
        "MS SQL Server Database Administrator", "Junior SQL DBA", "SQL Server Database Specialist", 
        "Freelance Database Engineer", "Database Architect", "Database Security Administrator", 
        "Applications Database Administrator", "Implementation, and Backup"
    ],
    "Yazılım ve Uygulama Geliştirme": [
        "Application Developer", "Web Developer/Programmer", "Software Engineer/Database Administrator", 
        "SQL Developer", "BI/SSRS Developer", "Business Intelligence Developer", 
        "Technical Application Administrator", "Scrum Master/Agile Coach", 
        "Blackboard Administrator/Systems Programmer", "Technical Support Analyst"
    ],
    "Analist ve Veri Uzmanları": [
        "Veri Analisti", "Veri Tabanı Analisti", "Veri Analitiği Mentoru", 
        "Database/Security Analyst", "Business Analyst for People Analytics", 
        "Financial Business Analyst", "Marketing Business Analytics Specialist", 
        "Business System Analyst", "Database Architect", "Data Warehouse Architect"
    ],
    "BT Destek ve Güvenlik": [
        "IT Support Technician", "IT Specialist II", "IT Service Rep", 
        "IT User Support Supervisor", "IT Manager/Programmer", 
        "IT Security Analyst", "Lead IT Security Compliance Analyst", 
        "IT Security Administrator", "System Administrator", 
        "Maintenance Administration Work Center Supervisor - Database/Systems Administrator", 
        "Aviation Maintenance Administration - Systems Administrator/Analyst", 
        "Junior AWS Cloud Solutions Architect", "AWS Architect", "AWS Cloud Engineer"
    ],
    "Havacılık ve Teknik Roller": [
        "Uçak Mekaniği/Veritabanı Yöneticisi", "Aircraft Mechanic", "Pilot in Training", 
        "Aviation Electronics Technician"
    ],
    "Proje ve Yönetim Rolleri": [
        "General Manager", "Director of IT", "Envanter Kontrol", 
        "Store Manager", "Sales Administrator", "Counter Intelligence Agent", 
        "Corp. Marketing Campaign Coordinator & Database Administrator", 
        "Production Lead"
    ],
    "Eğitim ve Mentorluk": [
        "Yazılım Dağıtım Teknisyeni ve Bilgisayar Bilimleri Öğretim Görevlisi", 
        "Lisansüstü Asistan", "Veri Analitiği Mentoru"
    ],
    "Veritabanı Yöneticisi ve Geliştiricisi": [
        "Oracle DBA/Developer", "SQL Database Administrator/DBA", 
        "Senior Oracle Database Administrator", "Oracle Lead Database Administrator", 
        "MySQL Database Administrator", "Oracle Database Administration", 
        "Oracle D2K Developer", "SQL Database Engineer", "MSSQL Database Administrator", 
        "Pricing Database Administrator", "SQL Server DBA", 
        "RM-BPO Order Entry Database Administrator", "Geospatial Database Administrator", 
        "SQL Veritabanı Yöneticisi II", "SQL Database Developer", 
        "Freelance SQL & Database Developer", "National Marketing Database Administrator", 
        "Developer and Database Administrator", "Contract Coordinator/Database Administrator", 
        "SharePoint Developer ve Database Administrator"
    ],
    "Yazılım ve Uygulama Geliştirme": [
        "Full Stack Developer/IT", "WordPress and Drupal Developer", 
        "WordPress SEO Specialist", "Cherwell Administrator", 
        "DevOps Developer for the Database Administration Team", 
        "Software Engineer/Support Escalation", "QA Engineer", "QA Tester", 
        "Reports Developer", "Obiee Developer", "Sr. Obiee Developer ve Administrator", 
        "Visual Basic Developer", "FoxPro Programmer", "BI Developer"
    ],
    "BT Destek ve Sistem Yönetimi": [
        "Head of IT Department / Systems and Database Administration", 
        "Systems and Database Administrator / IT Consultancy", 
        "Lead Systems Engineer", "IT Database Administrator", 
        "IT Database Consultant", "System Analyst", "Technical Support", 
        "IT Help Desk", "AWS Solution Architect/DevOps Engineer", 
        "AWS Infrastructure Engineer", "Sr. SharePoint Developer", 
        "Infrastructure Representative", "Cloud Network Engineer", 
        "Systems Engineer - Systems Administrator", "Desktop Support Administrator", 
        "Network Collection System Data Analyst"
    ],
    "Analist ve Veri Uzmanları": [
        "Cyber Security Analyst", "Senior Cyber Security Analyst", 
        "Security Controls Assessor", "Information and Database Specialist", 
        "Network Collection System Data Analyst", "Supply Chain Analyst", 
        "AML Risk Model and Analytics", "Marketing Data Resource Manager", 
        "Data Architect", "Research Analyst"
    ],
    "Yönetim ve Proje Yönetimi": [
        "Program Direktörü", "İşletme Operasyon Uzmanı", 
        "Program Yöneticisi", "Uyum Program Yöneticisi/Yönetici", 
        "Cloud Architect", "Project Manager/DBA", 
        "Program Assistant/Team Leader", "Client Success Manager/Account Manager", 
        "Community Engagement Manager", "Community Manager", 
        "Manager", "Co-Founder"
    ],
    "Eğitim ve Destek": [
        "Jr. Web Developer ve IT Instructor", "Graduate Research Assistant", 
        "Breastfeeding Peer Counselor", "Emzirme Danışmanı", 
        "Visitation Supervisor", "Ziyaret Denetmeni", "Uygunluk Yöneticisi"
    ],
    "Pazarlama ve İş Geliştirme": [
        "Business Developer", "Product Specialist", 
        "Marketing Intern", "Salesforce Administrator & Marketing Strategist", 
        "Marketing Manager", "Freelance Email Marketing Campaign Administration"
    ],
    "Hukuk ve İdari Roller": [
        "Legal Administrator Assistant", "Case Manager", 
        "Case Manager/Legal Assistant", "Claims Representative", 
        "Paralegal", "Contracts Manager/Legal Assistant", 
        "Legal Assistant", "Office Associate"
    ],
    "Veritabanı Yöneticisi ve Geliştiricisi": [
        "Database Administrator and Developer", "Database Administrator", 
        "Project Manager/Database Administrator", "Business Analyst / Database Administrator", 
        "SQL Server Database Admin/DBA/Analyst", "SQL Developer/Database Admin Support/Database Analyst", 
        "Lead DBA", "Database Administrator/Web Designer", "Sr. Database Administrator/Developer", 
        "Database Administrator / Data Analyst", "Executive Database Administrator", 
        "Oracle Database Administrator and Solutions Architect", 
        "Oracle Database & Banner Administrator", "Jr. Oracle Database Administrator"
    ],
    "Yazılım ve Uygulama Geliştirme": [
        "Full-Stack Engineer/Database Administrator", "Application Development Summer Intern", 
        "Web Designer", "Intern Web Developer", "Web Designer", "Junior Web Developer and IT Instructor"
    ],
    "BT Destek ve Sistem Yönetimi": [
        "IT Administrator", "IT Specialist/Intern", "Help Desk Administrator", 
        "Database/System Administrator", "Remote Helpdesk Technician", "Tier 3 Service Desk Technician", 
        "Technical Production Assistant", "IT Field Technician", "IT Support Analyst", 
        "Desktop Support", "Linux System Administrator/Database Admin Support", 
        "Database Assistant Administrator", "System Administrator Assistant", 
        "IT Support Assistant", "IT Manager/Database Administrator", "Cloud Operations Engineer Intern"
    ],
    "Veri Analisti ve İleri Düzey Analistler": [
        "Quality Assurance Manager", "Quality Assurance Inspector", "Reporting Specialist", 
        "Senior Database Analyst", "Data Analyst - Decision Support", "Health Care Data Analyst"
    ],
    "İş ve Proje Yönetimi": [
        "Program Director-Computer Information Science", "Project Manager/Database Administrator", 
        "Business Manager/Purchasing Coordinator", "Innovation Account Manager", 
        "Marketing/Merchandising Manager", "Marketing Coordinator", "Social Media & Communications Specialist", 
        "Customer Service Associate", "Customer Service/Sales", "Service Center Representative", 
        "Customer Service Officer", "Account Executive", "Client Support Specialist"
    ],
    "Veri Tabanı ve Bilgi Sistemleri": [
        "GIMS Database Administrator", "GIMS Specialist II", "Peoplesoft Database Administrator", 
        "GIS and Database Technician", "GIS Services", "CAD/Geographic Information Systems Technician"
    ],
    "Eğitim ve Staj": [
        "Cloud Operations Engineer Intern", "IT Internship/Database Administrator", 
        "Application Development Summer Intern", "Student Clerical Associate", 
        "Intern Web Developer", "Junior Network and Support Administrator"
    ],
    "Hukuk ve İdari Roller": [
        "External Fraud Investigator", "Student Clerical Associate", "Patient Care Technician", 
        "Client Service Officer", "Escrow Closing Specialist"
    ],
    "Pazarlama ve İş Geliştirme": [
        "Marketing and Operations Manager", "Freelance IT", "Freelance IT", "Diplomatic Security Officer/Console Operator"
    ],
    "Sağlık ve Sosyal Hizmetler": [
        "Patient Care Advocate", "Psychologist - Psychotherapist", "Social Welfare Manager"
    ],
    "Veritabanı Yöneticisi ve Geliştiricisi": [
        "Database Entry Administrator", "Database Developer/Administrator", "Database Developer/Analyst", 
        "Jr. Oracle DBA", "Oracle Apps Database Administrator", "Database Coordinator", 
        "Database Administrator/Analyst", "MySQL DBA", "MySQL Database Engineer", "MySQL Support DBA", 
        "Oracle/MSSQL Server Database Administrator", "Senior Oracle Database Administrator", 
        "Database Marketing Administrator", "Database Marketing/CRM Analyst", "Database Specialist II", 
        "Database Administrator/Web Designer", "Program Administrator", "Database Specialist & Compliancewire Administrator"
    ],
    "Yazılım Geliştirme ve Programlama": [
        "Applications Programmer Analyst", "SQL Developer/SSIS/SSRS Developer", "Senior IOS Developer", 
        "IOS Developer", "Junior IOS Developer", "Programmer/Analyst", "Senior Business Analyst", 
        "Software Tester/QA Analyst", "Agile Scrum Master", "Sr. Net Software Engineer", "Net Developer", 
        ".Net Developer/Database Administrator", "Jr. Software Engineer", "Applications Engineer", 
        "SSRS/SSIS Report Developer", "MS SQL Server Developer", "Jr. Data Engineer", "ETL Developer", 
        "Programmer/Analyst", "SQL BI Developer/DBA", "Software Support Analyst"
    ],
    "İş ve Proje Yönetimi": [
        "Program Director", "Project Manager/Database Administrator", "Program Manager", "Program Administrator", 
        "Project/Database Analyst", "Program Manager/HRIS Manager", "Project Manager/HRIS Implementation Consultant", 
        "Data Visualization Analyst", "Mailing and Database Analyst", "Business Systems Analyst Intern", 
        "Business Consultant", "Senior Consultant", "Lead Account Manager", "Client Success Team Member", 
        "Business Intelligence Analyst", "Program Analyst", "Product Development Administrator Director", 
        "Trust & Safety Specialist"
    ],
    "Veri Analizi ve İleri Düzey Analistler": [
        "Senior SQL DBA Consultant", "Senior Consultant", "Data Analyst Lead", "Data Analyst", 
        "Business Intelligence Analyst", "Database Developer/Analyst", "Database Developer/Analyst", 
        "Database Marketing/CRM Analyst"
    ],
    "BT Destek ve Sistem Yönetimi": [
        "IT Help Desk Assistant", "Service Desk Technician", "IT Support Analyst", "Tech Support / Network Infrastructure Analyst", 
        "Help Desk Tier II", "IT Administrator", "System Analyst/Network Administrator", "Senior Infrastructure & Operation Manager", 
        "Database Administrator", "IT Support Assistant", "Linux System Administrator", "Windows Systems Administrator", 
        "IT Analyst", "IT Infrastructure Manager", "Database/System Administrator", "System Analyst/Engineer", 
        "Network Operations Manager", "Support Engineer", "Database Specialist II", "SQL Database Cloud Engineer"
    ],
    "Hukuk ve İdari Roller": [
        "Legal Administrator Assistant", "Billing Coordinator", "Reconciliation Analyst", "Operations Specialist", 
        "Substitute Computer Technician", "Leasing Administrator & Staff Accountant", "Medical Records Coordinator", 
        "Office Support Associate & Record Administrator", "Accounting Administrative Assistant", "Client Support Supervisor", 
        "Client Success Team Member"
    ],
    "Müşteri Hizmetleri ve Satış": [
        "Sales Representative", "Inside Sales Associate", "Key Holder/Sales Representative", 
        "Customer Service/Sales", "Sales Consultant", "Customer Service Associate", 
        "Front Desk Associate", "Sales Representative", "Customer Support Supervisor", 
        "Sales/Consultant", "Leasing Administrator", "Customer Service Supervisor"
    ],
    "Veri Tabanı Güvenliği ve Yönetimi": [
        "Security Analyst", "Information Security Analyst", "Security Controls Assessor", 
        "Database Administrator/Security", "Security Analyst Intern", "Database Security Administrator"
    ],
    "Eğitim ve Öğretim": [
        "Student Teacher Grades Mathematics", "Graduate/Teaching Assistant", "Junior Data Engineer"
    ],
    "Havacılık ve Mühendislik": [
        "Aircraft Load Planner", "Electrical Engineer", "Tactical Power Generation Specialist"
    ],
    "Finans ve Muhasebe": [
        "Staff Accountant Accounts Payable", "Revenue Auditor", "Financial Advisor", "Insurance Agency Owner", 
        "Billing Coordinator", "Accounting Assistant II"
    ],
    "Veritabanı Yöneticisi ve Geliştiricisi": [
        "Oracle Database Application Support - Graduate Assistant", "Production Database Administrator", 
        "PL/SQL/Oracle Database Developer", "Senior Oracle/MySQL Database Administrator", 
        "Senior MySQL/SQL Server Database Administrator", "MySQL/SQL Server Database Administrator", 
        "Oracle DBA Consultant", "Oracle DBA/SQL Server DBA", "Senior Peoplesoft System Administrator and Oracle DBA", 
        "Peoplesoft Upgrade Specialist and System Administrator", "Peoplesoft Administrator/DBA", 
        "Database Software Engineer", "Database Developer/Administrator", "Operations Database Administrator", 
        "Database Administrator/Station Reconciliation Analyst", "Database Specialist and Network Administrator", 
        "Database Coordinator", "Salesforce Database Administrator/Project Manager", "Salesforce Administrator Consultant", 
        "Salesforce Consultant", "Database Master Administrator", "Database Specialist", "Database Architect",
        "Database Administrator/Analyst"
    ],
    "Yazılım Geliştirme ve Programlama": [
        "Junior Front-End Developer", "Entry-Level Web Developer", "Junior Database Developer", "Junior Data Engineer",
        "Programmer/Analyst", "Software Support Analyst", "Senior Software Engineer", "Application Support Specialist", 
        "Oracle Applications Programmer Analyst", "Business Applications Analyst", "Junior Programmer"
    ],
    "İş ve Proje Yönetimi": [
        "Project Manager", "Business Consultant", "Project Analyst", "Program Manager", "Program Administrator", 
        "Project/Database Analyst", "Strategic and Technical Sales Consultant", "Senior Solutions Consultant", 
        "Training Manager", "Program Coordinator", "Operations/Accounting Analyst", "Program Coordinator/Global Experience Director"
    ],
    "Veri Analizi ve İleri Düzey Analistler": [
        "Senior Database Analyst", "Senior Data Analyst", "Business Intelligence Administrator", "Data Warehouse Developer", 
        "BI Enterprise Data Warehouse Architect", "BI Infrastructure Administrator", "Business Intelligence Analyst", 
        "Reporting Systems Analyst", "Database Marketing Analyst", "Data Software Engineer", "Technical Data Analyst", 
        "Database Marketing/CRM Analyst", "Data Visualization Analyst"
    ],
    "BT Destek ve Sistem Yönetimi": [
        "Field Service Technician/Service Supervisor", "Help Desk Analyst/Office Assistant", "Database and Systems Administrator",
        "IT Specialist", "Help Desk/IT Support", "Technical Support", "Technical Host Support", "IT Help Desk Support", 
        "IT Department Head", "IT Infrastructure Support", "IT Support/Database Specialist", "IT Support Analyst", 
        "IT Support Assistant", "IT Analyst", "IT Project Coordinator", "IT Systems Administrator", "System Engineer"
    ],
    "Hukuk ve İdari Roller": [
        "Administrative Support Specialist", "Administrative Assistant", "Office Administrator/Corporate Receptionist", 
        "Corporate Receptionist - Administrative Assistant", "Office Administrator - Corporate Receptionist", 
        "Executive Administrative Assistant/Database Administrator", "Executive Coordinator of Human Resources", 
        "Administrative Specialist", "Administrative Assistant and Database Administrator", "Executive Assistant", 
        "Office Support Associate & Record Administrator"
    ],
    "Müşteri Hizmetleri ve Satış": [
        "Sales Representative", "Inside Sales Associate", "Sales Support Specialist", "Sales Associate", 
        "Sales Agent", "Client Success Team Member", "Client Intake/Scheduler", "Sales Consultant", 
        "Customer Service Representative", "Customer Service Manager", "Client/Service Charge Accountant", 
        "Property Management Bookkeeper", "Sales/Consultant", "Customer Support Supervisor"
    ],
    "Eğitim ve Öğretim": [
        "Public Speaking Instructor", "Training Manager", "Instructor", "Training Coordinator", 
        "Learning Management System Content Administrator", "LMS Administrator/Training Coordinator", 
        "Professor of Database Systems I", "Professor of Mathematics I", "E-learning Coordinator", "ICT Instructor", 
        "Career Advisor/Talent Recruiter", "Mentor"
    ],
    "Finans ve Muhasebe": [
        "Financial Analyst/HR Administrator", "Portfolio Accountant", "Accounts/Database Administrator", 
        "Accounts Payable Clerk", "Client Accountant", "Executive Assistant & Database/Market Administrator", 
        "Accounts Database Administrator"
    ],
    "Tedarik Zinciri ve Lojistik": [
        "Consultant - Supply Chain Management", "Global Strategic Sourcing Consultant", "Sourcing Analyst", 
        "MBA Supply Chain Consultant/Project Manager", "Logistics Analyst", "Supply Technician", 
        "Production Team Advisor", "Supply Chain Specialist"
    ],
    "Veritabanı Yöneticisi ve Geliştiricisi": [
        "Oracle Database Application Support - Graduate Assistant", "Production Database Administrator", 
        "PL/SQL/Oracle Database Developer", "Senior Oracle/MySQL Database Administrator", 
        "Senior MySQL/SQL Server Database Administrator", "MySQL/SQL Server Database Administrator", 
        "Oracle DBA Consultant", "Oracle DBA/SQL Server DBA", "Senior Peoplesoft System Administrator and Oracle DBA", 
        "Peoplesoft Upgrade Specialist and System Administrator", "Peoplesoft Administrator/DBA", 
        "Database Software Engineer", "Database Developer/Administrator", "Operations Database Administrator", 
        "Database Administrator/Station Reconciliation Analyst", "Database Specialist and Network Administrator", 
        "Database Coordinator", "Salesforce Database Administrator/Project Manager", "Salesforce Administrator Consultant", 
        "Salesforce Consultant", "Database Master Administrator", "Database Specialist", "Database Architect",
        "Database Administrator/Analyst"
    ],
    "Yazılım Geliştirme ve Programlama": [
        "Junior Front-End Developer", "Entry-Level Web Developer", "Junior Database Developer", "Junior Data Engineer",
        "Programmer/Analyst", "Software Support Analyst", "Senior Software Engineer", "Application Support Specialist", 
        "Oracle Applications Programmer Analyst", "Business Applications Analyst", "Junior Programmer"
    ],
    "İş ve Proje Yönetimi": [
        "Project Manager", "Business Consultant", "Project Analyst", "Program Manager", "Program Administrator", 
        "Project/Database Analyst", "Strategic and Technical Sales Consultant", "Senior Solutions Consultant", 
        "Training Manager", "Program Coordinator", "Operations/Accounting Analyst", "Program Coordinator/Global Experience Director"
    ],
    "Veri Analizi ve İleri Düzey Analistler": [
        "Senior Database Analyst", "Senior Data Analyst", "Business Intelligence Administrator", "Data Warehouse Developer", 
        "BI Enterprise Data Warehouse Architect", "BI Infrastructure Administrator", "Business Intelligence Analyst", 
        "Reporting Systems Analyst", "Database Marketing Analyst", "Data Software Engineer", "Technical Data Analyst", 
        "Database Marketing/CRM Analyst", "Data Visualization Analyst"
    ],
    "BT Destek ve Sistem Yönetimi": [
        "Field Service Technician/Service Supervisor", "Help Desk Analyst/Office Assistant", "Database and Systems Administrator",
        "IT Specialist", "Help Desk/IT Support", "Technical Support", "Technical Host Support", "IT Help Desk Support", 
        "IT Department Head", "IT Infrastructure Support", "IT Support/Database Specialist", "IT Support Analyst", 
        "IT Support Assistant", "IT Analyst", "IT Project Coordinator", "IT Systems Administrator", "System Engineer"
    ],
    "Hukuk ve İdari Roller": [
        "Administrative Support Specialist", "Administrative Assistant", "Office Administrator/Corporate Receptionist", 
        "Corporate Receptionist - Administrative Assistant", "Office Administrator - Corporate Receptionist", 
        "Executive Administrative Assistant/Database Administrator", "Executive Coordinator of Human Resources", 
        "Administrative Specialist", "Administrative Assistant and Database Administrator", "Executive Assistant", 
        "Office Support Associate & Record Administrator"
    ],
    "Müşteri Hizmetleri ve Satış": [
        "Sales Representative", "Inside Sales Associate", "Sales Support Specialist", "Sales Associate", 
        "Sales Agent", "Client Success Team Member", "Client Intake/Scheduler", "Sales Consultant", 
        "Customer Service Representative", "Customer Service Manager", "Client/Service Charge Accountant", 
        "Property Management Bookkeeper", "Sales/Consultant", "Customer Support Supervisor"
    ],
    "Eğitim ve Öğretim": [
        "Public Speaking Instructor", "Training Manager", "Instructor", "Training Coordinator", 
        "Learning Management System Content Administrator", "LMS Administrator/Training Coordinator", 
        "Professor of Database Systems I", "Professor of Mathematics I", "E-learning Coordinator", "ICT Instructor", 
        "Career Advisor/Talent Recruiter", "Mentor"
    ],
    "Finans ve Muhasebe": [
        "Financial Analyst/HR Administrator", "Portfolio Accountant", "Accounts/Database Administrator", 
        "Accounts Payable Clerk", "Client Accountant", "Executive Assistant & Database/Market Administrator", 
        "Accounts Database Administrator"
    ],
    "Tedarik Zinciri ve Lojistik": [
        "Consultant - Supply Chain Management", "Global Strategic Sourcing Consultant", "Sourcing Analyst", 
        "MBA Supply Chain Consultant/Project Manager", "Logistics Analyst", "Supply Technician", 
        "Production Team Advisor", "Supply Chain Specialist"
    ],
   "Veritabanı Yöneticisi ve Geliştiricisi": [
        "Veritabanı Yöneticisi/Yardım Masası Görevlisi", "Database Administrator ve Uygulama Tasarımcısı",
        "Platinum Patching Engineer/DBA", "Veritabanı Yöneticisi ve Uygulama Tasarımcısı", "Remote DBA/Team Lead",
        "Operational DBA", "Application DBA & ETL Developer", "Database Administrator and QA Tester",
        "Senior SQL Server/Oracle DBA/ETL Engineer", "Senior Oracle/SQL Server Database Administrator", 
        "Senior Systems Engineer/Database Administrator", "Political Surveyor Database Administrator"
    ],
    "Yazılım Geliştirme ve Programlama": [
        "Java Back-End Developer", "Freelance iOS Developer", "Software Engineer", "Java Developer", 
        "Java J2EE Developer", "Java Technical Lead", "Senior Java/J2EE Developer", "Java J2EE Developer",
        "Freelance/Contract Work", "Embedded Database Engineer", "Software Development Engineer"
    ],
    "Proje ve İş Yönetimi": [
        "Proje Yöneticisi/ Teknik Destek Sorumlusu", "Proje Yöneticisi", "Proje Yöneticisi ve İş Analisti",
        "Scrum Master", "Agile Project Manager", "Delivery Manager", "Teknik Proje Yöneticisi", "Manager III / Project Owner",
        "Program Test Uzmanı", "Project/Business Analyst", "IT Project Manager", "IT Project Coordinator",
        "Senior IT Project Manager", "Solution Architect", "Manager & Bartender", "Solution Consultant"
    ],
    "Veri ve İş Analizi": [
        "İş Analisti/Scrum Master", "Kıdemli İş ve Veri Analisti", "Kıdemli İş/ERM Analisti", 
        "İş Analisti ve Test Uzmanı", "Kıdemli İş Analisti", "Kıdemli İş Sistemi Analisti", 
        "Senior Business Analyst", "Senior Data Analyst", "Kıdemli İş Analisti / Scrum Master", 
        "Kıdemli İş Analisti / QA Analisti", "Business Analyst", "Database Analyst/Accounts Receivable"
    ],
    "Müşteri Hizmetleri ve Destek": [
        "Müşteri Hizmetleri Temsilcisi", "Müşteri Destek Yöneticisi", "Customer Support Specialist", 
        "Help Desk", "IT Help Desk Support", "Customer Service/Host", "Customer Service/Human Resources Representative",
        "Customer Service Representative/Cashier"
    ],
    "Kalite ve Lojistik": [
        "Quality Assurance Specialist", "Quality Technician", "Quality Engineer", "ISO Management Representative",
        "Quality & Logistics Manager", "Logistics Analyst", "İthalat Lojistik Koordinatörü", "Quality Technician",
        "Logistics Analyst"
    ],
    "BT Destek ve Güvenlik": [
        "IT Support Specialist", "IT Security Analyst/Fraud Prevention Analyst", "IT Operations Administrator", 
        "Help Desk Support/Programmer/SQL Database Administrator", "Cyber Privacy and Security Analyst", 
        "Database and Systems Administrator", "Database Administrator/Administrative Contractor", 
        "Operations Database and SQL ETL Administrator"
    ],
    "İdari ve Ofis Destek": [
        "Administrative Multi-Line Representative", "Administrative Coordinator", "Office Administrator", 
        "Program Assistant", "Administrative Assistant", "Print Specialist", "Technical Administrative Assistant",
        "Secretary II", "Integration Specialist", "Administrative Specialist", "Office Support Associate & Record Administrator"
    ],
    "Eğitim ve Öğretim": [
        "STEM Eğitmeni", "Learning Database Administrator/Administrative Contractor", "Foreign Teacher Assessor", 
        "Certified Nursing Assistant", "Instructor", "Volunteer", "Yoga Instructor"
    ],
    "Satış ve İş Geliştirme": [
        "Business Development Manager", "National Sales Administrator/Database Administrator", 
        "Director of Sales", "Director of Sales Operations", "Sales Manager", "Sales Representative",
        "Sales Agent", "Customer Support Representative", "Accounts Manager", "Client Intake/Scheduler"
    ],
    "Finans ve Muhasebe": [
        "Personal Banker I", "Account Services Administrator", "Accounts Payable Administrator", 
        "Entry Level Bookkeeper", "Budget Technician", "Budget Analyst Assistant", "Client Accountant"
    ],
    "Yazılım Geliştirme ve Mühendislik": [
        "Java Geliştirici", "Java full stack geliştirici", "Java/j2ee geliştirici", "Java programcısı",
        "Java teknik lideri", "Java çözüm mimarı", "Java/ui geliştirici", "Java tam yığın geliştiricisi", 
        "Java spring angular geliştirici", "Java ön uç geliştirici", "Java geliştiricisi/mimar", 
        "Full Stack Geliştirici", "Full stack java geliştiricisi", "Full stack java/j2ee geliştiricisi", 
        "Full stack java geliştiricisi", "Yazılım Mühendisi", "Yazılım mühendisi", "Yazılım test mühendisi",
        "Yazılım mühendisliği", "Yazılım QA test mühendisi", "Yazılım geliştiricisi", "Kıdemli yazılım geliştiricisi", 
        "Mikroservis Geliştiricisi", "Mikroservis geliştiricisi", "PHP Geliştirici", "PHP geliştiricisi", 
        "Kıdemli php/drupal geliştiricisi"
    ],
    "İş Analisti ve Proje Yönetimi": [
        "İş Analisti", "Kıdemli iş analisti", "İş sistemi analisti", "İş analisti/scrum master", 
        "İş analisti ve proje yöneticisi", "İş analisti/proje yöneticisi", "İş analisti danışmanı",
        "Proje Yönetimi", "Proje yöneticisi", "Proje lideri", "Proje koordinatörü", "Proje yöneticisi/scrum master", 
        "Proje yöneticisi/iş analisti", "Proje yöneticisi/qa test yöneticisi", "Proje lideri/sürüm yöneticisi",
        "Scrum Master", "Scrum master", "Scrum master/proje yöneticisi", "Scrum master/qa test yöneticisi", 
        "Scrum master/iş analisti", "Agile ve Çevik Yönetim", "Agile scrum master", "Çevik program yöneticisi", 
        "Scrum uzmanı", "Agile project manager"
    ],
    "Test ve Kalite Güvencesi": [
        "Test Uzmanı", "Test uzmanı", "QA test uzmanı", "QA mühendisi", "Test mühendisi", "Program test uzmanı",
        "Yazılım test mühendisi", "Kıdemli test mühendisi", "Kalite Güvencesi", "Kalite güvence test uzmanı", 
        "Kalite analisti", "Kalite ve iş analisti", "Kalite yöneticisi", "Test lideri", "QC lideri", "QA lideri", 
        "Test Yönetimi", "Test yöneticisi", "Test lideri", "QA proje yöneticisi", "QA proje lideri"
    ],
    "Veritabanı ve Sistem Yönetimi": [
        "Veritabanı Yöneticisi", "Veritabanı yöneticisi", "Veritabanı ve uygulama tasarımcısı", 
        "Oracle veritabanı yöneticisi", "SQL veritabanı yöneticisi", "Sistem Yönetimi", "Sistem yöneticisi", 
        "IT destek uzmanı", "Teknik destek mühendisi", "BT proje yöneticisi", "Sistem çözüm mühendisi/altyapı yöneticisi", 
        "Altyapı hizmet yöneticisi"
    ],
    "Danışmanlık ve Çözüm Mühendisliği": [
        "Teknik Danışmanlık ve Çözüm Mühendisliği", "Çözüm mimarı", "Teknik danışman", "ERP danışmanı", 
        "Teknoloji geçiş lideri", "BT tedarik zinciri danışmanı", "Tedarik zinciri çözüm yöneticisi", "Danışman/dba",
        "Fonksiyonel Danışmanlık", "SAP iş sistemleri analisti", "SAP modül danışmanı", "İş analisti/sap sd modülü", 
        "İş analisti/sap isu ccs-faturalama ve fatura kesme fonksiyonel danışmanı"
    ],
    "Veri Analizi ve İş Zekası": [
        "Veri Analisti", "Veri analisti", "İş veri analisti", "Veritabanı analisti", "Veritabanı yönetim analisti", 
        "Veri bilimcisi", "BI (iş zekası) raporlama lideri", "BI (iş zekası) mimar", "Veri analisti/veri yöneticisi", 
        "İş Zekası (BI) ve Raporlama", "BI (iş zekası) raporlama lideri", "BI mimar", "Veri analizi ve iş zekası uzmanı"
    ],
    "Ekip Liderliği ve Yönetim": [
        "Ekip Liderliği", "Ekip lideri", "Kıdemli ekip lideri", "Teknik ekip lideri", "Scrum master/lider iş analisti", 
        "Kıdemli proje yöneticisi", "Kıdemli yazılım mühendisi", "Yönetim", "Yönetici", "Kıdemli yönetici", 
        "Proje yöneticisi", "Proje koordinatörü", "Satış müdürü", "Operasyonel yönetici"
    ],
    "İleri Seviye Teknik ve BT Uzmanlık": [
        "İleri Seviye BT Uzmanlık", "Kıdemli yazılım mühendisleri", "Senior full-stack java developer", 
        "Kıdemli veri mimar", "Kıdemli teknik proje yöneticisi", "Sistem analisti", "IT güvenlik analisti", 
        "Risk analisti", "Hadoop admin", "Embedded database engineer", "BT Proje Yönetimi ve İleri Teknik Yönetim", 
        "BT proje yöneticisi", "BT yöneticisi", "Teknik lider", "Teknoloji uzmanı", "IT operasyon yöneticisi"
    ],
    "Destek ve İdari Rolleri": [
        "Destek Rolleri", "Yardım masası görevlisi", "Müşteri hizmetleri temsilcisi", "IT destek uzmanı", 
        "Yardım masası görevlisi", "Ofis destek uzmanı", "İdari Rolleri", "İdari koordinatör", "İdari asistan", 
        "Ofis yöneticisi", "İdari personel"
    ],"Yazılım Geliştirme ve Mühendislik": [
        "Technical Engineer", "Full-Stack Web Developer", "ETL/Uygulama Geliştirici", "ETL Mühendisi", 
        "Applications Developer", "SQL Server Developer/Programmer", "Mobile Phone Sales Consultant", 
        "Blockchain Developer", "Software Developer Intern"
    ],
    "Veritabanı ve Sistem Yönetimi": [
        "Senior MongoDB DBA", "Senior Oracle Database Administrator", "Lead Database Administrator", 
        "Database Administrator", "Database Analyst", "Database Administrator & Web Developer", 
        "SQL Server DBA Production Support", "DB2 Database Administrator", "Microsoft SQL Database Administrator", 
        "MongoDB Admin/Oracle Database Admin", "SQL Server Engineer/DBA", "Database Specialist", 
        "Database Developer", "Database Services Consultant", "Database Administrator/Reporting Analyst", 
        "Database Administrator / Recruiter", "Senior Database Administrator", "Database Administrator / Recruiter"
    ],
    "Destek ve İdari Rolleri": [
        "Development Associate to Executive Office", "Assistant Office Administrator", "IT Systems Administration Intern", 
        "Executive Assistant/Executive Receptionist", "Administrative Assistant", "Administrative Assistant to the Director of Maintenance & Engineering",
        "Administrative Assistant/Executive Assistant/Executive Receptionist", "Project Assistant", "Administrative Assistant II",
        "Assistant Database Administrator Intern", "Administrative Assistant to the Director of Operations", "Executive Assistant", 
        "Executive Receptionist", "Project Development Designer", "Project Development Specialist"
    ],
    "Müşteri ve Satış Destek": [
        "Customer Service Representative", "Retail Sales Representative", "Customer Service Associate", "Customer Service Agent", 
        "Customer Service Analyst", "Customer Support Representative", "Customer Service Assistant", "Retail Sales Consultant",
        "Business Data Analyst", "Business Data Analyst- Tableau Reporting Intern"
    ],
    "Pazarlama ve Dijital Reklam": [
        "Digital Ad Ops Associate", "Digital Marketing Intern", "Digital Marketing Manager", "Social Media Intern", 
        "Brand Identity Design Freelancer", "Sales & Marketing Associate", "Design & Marketing Manager", 
        "Sales Assistant", "Sales Person", "Event Specialist/Merchandiser"
    ],
    "Veri Analizi ve İş Zekası": [
        "Data & Business Analyst", "Data Analyst", "SQL/BI Developer", "Reporting Analyst", "Data Analyst & Database Administrator",
        "M&E Officer", "Business Application Developer", "Data & Business Analyst", "Supply Control & Production Analyst"
    ],
    "Proje Yönetimi ve İleri Seviye Yönetim": [
        "Project Recruiter", "Project Manager", "Project Coordinator", "Scrum Master/Project Manager", "Scrum Master", 
        "Project Coordinator/Scrum Master", "Program Administrator", "Project Development Manager", "Project Manager/Business Analyst"
    ],
    "Ekip Liderliği ve Yönetim": [
        "Team Lead", "Senior Distribution Manager", "Platform Solutions Analyst", "Platform Operations Analyst", 
        "Logistics Coordinator", "Warehouse Manager", "Operations Excellence Manager", "Senior Data Analyst", 
        "Service Desk Analyst", "Operations Manager"
    ],
    "Sistem ve Güvenlik": [
        "IT Systems Administrator", "IT Security Analyst", "Information System Security Officer", "Security Control Assessor/Analyst", 
        "Lead IT Security Analyst", "Cyber Security Analyst", "System Designer", "IT Solutions Architect", "Windows System Administrator", 
        "Incident Manager"
    ],
    "Eğitim ve Danışmanlık": [
        "Teacher", "Instructor", "Teaching Assistant", "Education Director", "Student Engagement Specialist", "Youth Educator", 
        "Student Program Administrator", "Graduate Teaching Assistant", "Peer Academic Advisor"
    ],
    "Gönüllülük ve Sosyal Çalışmalar": [
        "Volunteer Tax Preparer", "Volunteer", "Social Work Professional", "Volunteer Tax Preparer", "Event Volunteer", 
        "Social Media Volunteer", "Media Team/Volunteer", "Research & Communications Intern"
    ],"Yönetim ve Liderlik": [
        "Mağaza Müdürü",
        "Ekip Liderliği ve Yönetim",
        "Proje Yönetimi ve Liderlik",
        "Yönetim ve Proje Yönetimi",
        "İleri Seviye İdari Pozisyonlar"
    ],
    "Teknik ve Bilgi Teknolojileri": [
        "3D Artist",
        "AWS Architect",
        "Avionic Systems Repairer",
        "IT Professional",
        "IT Service Rep",
        "Oracle Dba",
        "Network Engineer",
        "Web Developer",
        "Database Administrator (DBA)",
        "Cloud Practitioner"
    ],
    "Sanat ve Yaratıcılık": [
        "Sanat ve Yaratıcılık",
        "Fotoğrafçılık ve Medya",
        "Etkinlik Videografı/Editörü",
        "Grafik Tasarımcı",
        "İç Mimar",
        "Sanat Eğitmeni"
    ],
    "Sağlık ve Sosyal Hizmetler": [
        "Sağlık ve Bakım",
        "Sağlık ve Sosyal Hizmetler",
        "Masaj Terapisti",
        "Gönüllü Masaj Terapisti",
        "Sosyal Hizmetler Danışmanı"
    ],
    "Eğitim ve Akademik": [
        "Öğretim Görevlisi",
        "Professor of Mathematics",
        "Eğitim Yardımcısı",
        "Eğitim Koordinatörü"
    ],
    "Müşteri İlişkileri ve Destek": [
        "Müşteri ve Kalite Destek",
        "Müşteri İlişkileri ve İletişim",
        "Müşteri Destek",
        "Call Center Representative",
        "Ticket Support"
    ],
    "Lojistik ve Dağıtım": [
        "Lojistik ve Operasyon",
        "Taşımacılık ve Dağıtım",
        "Kargo Dağıtımı",
        "Depo Sorumlusu",
        "Dağıtım Şoförü"
    ],
    "Finans ve Muhasebe": [
        "Finans ve Muhasebe",
        "Mali Muhasebeci",
        "Vergi Danışmanı",
        "Finansal Analist",
        "Satın Alma ve Tedarik Uzmanı",
        "Banka Memuru"
    ],
    "Hukuk ve İdari": [
        "Hukuk ve İdari Roller",
        "Avukat",
        "Paralegal",
        "İcra Memuru"
    ],
    "İnsan Kaynakları ve Yönetim": [
        "İnsan Kaynakları ve Yönetim",
        "İK Uzmanı",
        "Eğitim ve Gelişim Uzmanı",
        "İK Danışmanı"
    ],
    "Gönüllü ve Sosyal Hizmetler": [
        "Gönüllü ve Topluluk Hizmeti",
        "Gönüllülük ve Sosyal Çalışmalar",
        "Toplum Temsilcisi",
        "Sosyal Hizmetler Yardımcısı"
    ],
    "Tasarım ve Kullanıcı Deneyimi": [
        "UX Tasarımcısı",
        "UI/UX Developer",
        "Grafik Tasarımcı",
        "Endüstriyel Tasarımcı"
    ],"Veri ve Analitik": ['Veri Ambarı ve İş Zekası', 'Veri Analizi ve Araştırma', 'Veri Analizi ve İş Zekası', 'Veri Tabanı Güvenliği ve Yönetimi', 'Veri Tabanı ve Bilgi Sistemleri', 'Veri ve İş Analizi', 'Veritabanı ve Sistem Yönetimi', 'administrative and database assistant', 'corporate buying data assistant', 'data collector and processor', 'data entry clerk', 'data entry operator ii', 'data entry/scheduling', 'data migration assistant', 'data modeler/dba', 'data operator ii', 'data warehouse architect', 'database admin', 'database architect', 'database clerk', 'database development', 'database development its', 'datalisansse processor', 'junior sql dba', 'kıdemli sql server dba', 'ms sql admin', 'ms sql dba', 'ms sql server dba', 'mssql dba', 'mysql dba', 'nttdata-customer service rep', 'operasyonel sql dba', 'oracle database administration', 'oracle database architect/admin', 'oracle dba/sql server dba', 'oracle ve aws veri̇tabani yöneti̇ci̇si̇', 'practice development interaction da   ata steward', 'principal data architect', 'professor of database systems i', 'program veri asistanı', 'senior sql dba', 'shipyard contracts database assistant', 'sql dba', 'sql server database dba/admin', 'sql server dlisans', 'sql server dlisans ii', 'sql server/ms access veri̇tabani yöneti̇ci̇si̇', 'sql sever dba', 'sql- dlisans', 'sr. data architect', 'sr. ms sql server dba', "sr. oracle and sql server dba", 'sr. sql server dba', 'sr. sql server ve mongodb dba', 'veri girişi görevlisi', 'veri tabanı görevlisi / müşteri hizmetleri', 'veritabanı koordinatörü', 'veri̇tabani destek tekni̇syeni̇'],
    "Teknisyen": ['bilgi güvenliği teknisyeni', 'cad/ geographic information systems technician', 'computer technician', 'database technician', 'dijital/e-ticaret koordinatörü teknisyeni', 'ekipman teknisyeni', 'fiber optik teknisyeni', 'field service representative / technician', 'field technician', 'hizmet tesisatçısı - baş teknisyen', 'it field technician', 'patient care technician', 'quality control technician', 'su arıtma teknisyeni', 'substitute computer technician', 'veri tabanı operatörü/teknisyeni'],
    "Uzman": ['Analist ve Veri Uzmanları', 'acquisition database specialist', 'advancement database analyst', 'all-source analyst', 'analyst', 'analyst of inside communication quality', 'application specialist', 'application support specialist', 'applications programmer analyst', 'architecture & application analyst', 'assistant consultant', 'associate consultant', 'ağ danışmanı', 'ağ ve uygulama uzmanı', 'benefit support specialist / tech support', 'bilgi analitiği uzmanı', 'bilgi sistemleri danışmanı', 'bt destek uzmanı', 'bt uzmanı', 'building maintenance specialist', 'business analyst for people analytics', 'business analyst intern', 'business analyst/risk analyst', 'business analyst/scrum master', 'business data analyst/scrum master', 'business system analyst', 'business system analyst-us', 'business systems analyst', 'business systems analyst intern', 'business systems analyst/scrum master', 'business/data analyst', 'business/requirements analyst', 'call center reporting specialist', 'cardiology systems analyst and access provisioning', 'career advisor / talent recruiter', 'client support specialist', 'computer consultant', 'computer specialist', 'computer support specialist', 'computer systems analyst/programmer - database support', 'consultant', 'consultant - technical implementation specialist', 'counterterrorism intelligence analyst/watch officer', 'crm analyst', 'crm/ project analyst', 'curriculum geliştirme uzmanı', 'cyber security analyst/rmf specialist', 'data analyst/data steward', 'data entry specialist', 'database analyst / developer', 'database analyst contractor', 'database and sysadmin consultant', 'database consultant/business analyst', 'database developer/analyst', 'database specialist ii', 'database/security analyst', 'documentation specialist', 'ecommerce business analyst', 'ehr consultant', 'escrow closing specialist', 'f-35 suitability analyst', 'financial advisor', 'financial analyst', 'financial business analyst', 'financial management specialist', 'finans pmo danışmanı', 'fulfillment specialist', 'functional analyst', 'functional area expert', 'functional consultant', 'gayrimenkul satış uzmanı', 'geliştirme entegrasyon test uzmanı', 'gis specialist', 'gis uzmanı', 'grant writer and database analyst', 'help desk analyst', 'hesap yönetimi uzmanı', 'high-threat integrated tracking system  specialist', 'hotel data entry specialist', 'i.t. system specialist', 'information technology database programmer analyst', 'intake specialist', 'intelligence analyst', 'internet marketing analyst', 'ipm uzmanı', 'is customer support analyst', 'it database consultant', 'it desktop support specialist', 'it destek uzmanı', 'it production operations specialist', 'it risk analyst', 'it security analyst / compliance', 'it specialist ii', 'it specialist/intern', 'it support/ database specialist', 'i̇nşaat destek uzmanı', 'i̇ş akışı uzmanı', 'i̇ş analisti/danışmanı', 'i̇ş sistemleri uzmanı', 'java consultant', 'java danışmanı', 'java/j2ee   e danışmanı', 'jr. business analyst', 'jr. programmer analyst/java developer', 'kıdemli java danışmanı', 'kıdemli java/j2ee geliştirici danışmanı', 'kıdemli veri tabanı uzmanı', 'lisansckground verification specialist', 'mailing and database analyst', 'management analyst', 'marketing business analytics specialist', 'masaüstü destek uzmanı', 'membership intake program specialist', 'open source/research analyst', 'operations and branding consultant', 'operations specialist', 'oracle dba consultant', 'oracle product specialist / junior dlisans', 'oyun danışmanı', 'pricing analyst', 'procurement specialist', 'product specialist', 'production analyst', 'program analyst', 'programmer/analyst', 'project management quality specialist', 'project/ database analyst', 'qa analyst', 'quality analyst/junior business analyst', 'quality assurance analyst', 'raporlama uzmanı', 'reconciliation analyst', 'recreational specialist', 'remedy consultant', 's-2 intelligence analyst', 'salesforce consultant', 'sap hcm consultant', 'satış danışmanı', 'satış çözüm destek uzmanı', 'scrum master/report analyst', 'scrum master/sr. business analyst', 'security control assessor/ analyst', 'security operation center  analyst', 'senior analyst - clinical operations', 'senior analyst ii', 'senior consultant', 'senior consultant - contract', 'senior database consultant', 'senior java jee consultant', 'senior sql dba consultant', 'senior technical specialist', 'servis uzmanı', 'six sigma business analyst', 'social media & communications specialist', 'software engineering - qa analyst', 'software specialist', 'software support analyst', 'software tester/qa analyst', 'sql database admin/analyst', 'sql developer/database admin support/database analyst', 'sql server database admin/dba/analyst', 'sql server database specialist', 'sql server database specialist/dba', 'sql server dba consultant', 'sr it consultant contractor', 'sr. business analyst', 'sr. business analyst/aml business analyst', 'sr. business analyst/scrum master', 'sr. business consultant', 'sr. business system analyst', 'sr. business systems analyst', 'sr. business systems analyst/scrum master', 'sr. database marketing/ops analyst', 'sr. financial analyst', 'sr. it analyst/scrum master', 'sr. java jee consultant', 'sr. java jee consultant/application architect', 'sr. java/j2ee consultant', 'sr. solutions consultant', 'sr. specialist developer', 'staff consultant', 'summer financial analyst', 'support center analyst', 'system analyst', 'system analyst/engineer', 'systems analyst', 'systems analyst/project engineer', 't-sql developer/programmer analyst', 'tech support / network infrastructure analyst', 'technical analyst 1', 'technical support analyst', 'technical support specialist', 'techno - functional consultant', 'technology analyst-us', 'technology specialist', 'tedarik zinciri danışmanı', 'teknik destek danışmanı', 'teknik destek uzmanı', 'testing consultant / temporary associate', 'tier ii software support analyst', 'trust & safety specialist', 'trv specialist', 'veri giriş uzmanı', 'veri hizmetleri danışmanı', 'veri tabanı uzmanı', 'veritabanı destek uzmanı', 'veritabanı uzmanı ve kullanıcı destek analisti', 'veritabanı yönetimi uzmanı', 'wordpress seo specialist', 'yönetilen hizmet dba danışmanı', 'çağrı destek teknik uzmanı', 'İleri Seviye Teknik ve BT Uzmanlık'],
    "Staj ve Giriş Seviyesi Roller": ['junior aws cloud solutions architect', 'junior counselor', 'junior dba', 'junior oracle dba'],
    "İdari ve Destek Rolleri": ['Müşteri Hizmetleri ve Destek', 'Müşteri Hizmetleri ve Perakende', 'account services assistant', 'account/customer service representative', 'accounting administrative assistant', 'admin gudang', 'administration assistant', 'assistant accountant', 'assistant architectural photographer', 'bilingual receptionist', 'business services representative - receptionist', 'cassandra admin', 'clerical aide', 'client service officer', 'commissioned security officer', 'computer vision project assistant', 'cosmos db admin', 'customer service / host', 'customer service / human resources representative', 'deli associate/customer service/janitorial', 'direktör asistanı', 'eam administrative assistant', 'graduate assistant', 'graduate/teaching assistant', 'graphics design assistant', 'it officer', 'i̇dari asistaan', 'i̇şletme asistanı ii', 'kıdemli i̇dari asistan', 'legal assistant', 'müşteri hizmetleri telisansilcisi', 'office admin', 'office assistant', 'office associate',   'office receptionist/vet assistant', 'ofis asistanı', 'organizasyon asistanı', 'orientation week assistant', 'program assistant ii', 'proje asistanı', 'purchasing admin assistant', 'receptionist', 'security officer', 'senior administrative assistant', 'sysadmin', 'technical production assistant'],
    "Teknik Destek": ['BT Destek ve Güvenlik', 'BT Destek ve Sistem Yönetimi', 'BT ve Teknik Destek', 'Teknik Destek ve Operasyon', 'Teknik Destek ve Sistem Yönetimi', 'advanced technical support', 'airline it support', 'bilingual teknik destek analisti', 'bt yardım masası', 'desktop engineer', 'desktop support', 'front desk agent', 'front desk associate', 'front desk clerk', 'help desk technician', 'help desk tier ii', 'intern - it support', 'internet help desk support', 'it help desk', 'it help desk assistant', 'it support help desk', 'it support technician', 'medical assistant/front desk', 'program assistant/ front desk associate', 'service desk technician', 'technical support representative', 'teknik destek', 'teknik destek ekip lideri', 'teknik destek mühendisi', 'tier 3 service desk technician', 'yardım masası destek', 'yardım masası görevlisi'],
    "Mühendis": ['Danışmanlık ve Çözüm Mühendisliği', 'Havacılık ve Mühendislik', 'Veri Mühendisi', 'Yazılım Geliştirme ve Mühendislik', 'Yazılım Mühendisi', 'alan mühendisi', 'alan servisi mühendisi', 'applications engineer', 'assistant engineer bio medical equipment', 'assistant systelisans engineer', 'assistant system engineer trainee', 'associate software engineer', 'audio engineer', 'audio engineer intern', 'audio engineer volunteer', 'automotive relocation engineer', 'aws cloud engineer', 'aws infrastructure engineer', 'aws solution architect/devops engineer', 'ağ destek mühendisi', 'ağ mühendisi', 'baş mühendis', 'baş yazılım mühendisi', 'chemical engineering lab assistant', 'cloud network engineer', 'cloud security engineer', 'contract installation/network technician', 'database and linguistics engineer', 'database software engineer', 'dba/automation engineer', 'field service engineer', 'freelance database engineer', 'industrialization engineer', 'infrastructure engineer', 'innovation team engineer', 'it destek mühendisi', 'it/engineering technical recruiter', 'i̇nşaat otomasyon mühendisi', 'junior data engineer', 'junior software engineer',  'kıdemli mühendis', 'kıdemli veritabanı mühendisi', 'lisansüstü mühendis stajyeri', 'manufacturing engineering intern', 'mağaza sistem mühendisi', 'mysql database engineer', 'müşteri mühendisi', 'network engineer / programmer', 'network technician', 'nodal network systems operator-maintainer instructor', 'oracle database engineer', 'oracle database senior technical engineer', 'orta yazılım geliştirme mühendisi', 'os patch build engineer', 'performans mühendisi', 'personel yazılım mühendisi', 'principal engineer', 'product support engineer', 'proje lideri / kıdemli yazılım mühendisi', 'project engineer', 'qa engineer', 'rf engineer', 'rf mühendisi', 'saha mühendisi', 'senior qa automation engineer', 'senior software engineer', 'servicenow engineer', 'software engineer/support escalation', 'software engineering - qa intern', 'software support engineer', 'software test engineer', 'sql database cloud engineer', 'sql database engineer', 'sql dba/azure cloud data engineer', 'sr. software engineer/application architect', 'sr.net software engineer', 'subsurface utility engineering tech', 'support engineer', 'systelisans engineer', 'systems engineer', 'systems engineer 2', 'systems engineer/devops engineer', 'trainee software engineer', 'unified communications engineer', 'yapı ve yayın mühendisi', 'yazılım mühendisi/trainee', 'yazılım otomasyon test mühendisi', 'yazılım qa test mühendisi'],
    "Analist": ['Analist', 'Veri Analisti ve İleri Düzey Analistler', 'Veri Analizi ve İleri Düzey Analistler', 'Veritabanı Analisti ve Veri Yönetimi', 'analist programcı', 'ba/qa analisti', 'baş pmo analisti', 'baş teknik i̇ş sistemi analisti', 'bt analisti', 'finans analisti', 'it analisti', 'it güvenlik analisti/fraud önleme analistii', 'it uygulamaları analisti', 'i̇ş analisti / danışman', 'i̇ş analisti / scrum master', 'i̇ş analisti stajyer', 'i̇ş analisti ve proje yönetimi', 'i̇ş analisti/kalit    te analisti', 'i̇ş sistem analisti', 'i̇ş sistemi analisti / i̇ş analisti', 'i̇ş sistemi/qa analisti', 'i̇ş sistemleri analisti', 'i̇ş sistemleri analisti / scrum mast     ter', 'i̇ş teknolojisi analisti / veri analisti', 'i̇ş/kalite analisti', 'jr. i̇ş analisti', 'kalite ve i̇ş analisti', 'kalite/i̇ş analisti', 'kıdemli düzenleyici anal    list', 'kıdemli i̇ş analisti/ scrum master', 'kıdemli i̇ş analisti/proje koordinatörü', 'kıdemli i̇ş analisti/scrum master', 'kıdemli i̇ş kalite analisti', 'kıdemli i̇    ş sistem analisti', 'kıdemli i̇ş sistemi analisti / lider i̇ş analisti', 'kıdemli i̇ş sistemi analisti/ scrum master', 'kıdemli i̇ş sistemi analisti/veri analisti','kıdemli i̇ş sistemleri analisti', 'kıdemli teknik i̇ş sistemi analisti', 'kıdemli teknik i̇ş sistemi analisti / bi raporlama lideri', 'kıdemsiz i̇ş analisti', 'lider     i̇ş sistemleri analisti', 'lojistik analisti', 'margin proje analisti', 'ms-sql veri analisti ve dba', 'oracle veritabanı analisti', 'pm / kıdemli analist', 'program  analisti', 'proje analisti', 'raporlama sistemleri analisti', 'restoran teknolojisi analisti', 'sap i̇ş sistemleri analisti', 'sağlık hizmetleri i̇ş analisti', 'sağlı ık veri analisti', 'scrum master / i̇ş analisti', 'scrum master / lider i̇ş analisti', 'scrum master/i̇ş analisti', 'serbest araştırma analisti', 'siber güvenlik anali  isti', 'sql server i̇ş verisi analisti', 'sr. i̇ş sistemleri analisti', 'teknik analist', 'teknik lider ve analist', 'uygulama analisti', 'veri ambarı analisti', 'veri i analisti', 'veri analisti / uygulama destek', 'veri tabanı analisti', 'veri taşıma analisti', 'veri ve e-ticaret analisti', 'veritabanı analisti', 'çözüm analisti', 'ürün sahibi/i̇ş analisti', 'İş Analisti ve Proje Yönetimi'],
    "Geliştirici": ['.net developer', 'Backend Geliştirici', 'Full Stack Geliştirici', 'Java Geliştirici', 'Yazılım Geliştirici', 'Yazılım Geliştirme ve Programlama', 'Yazılım ve Dijital Çözümler', 'Yazılım ve Uygulama Geliştirme', 'analist/geliştirici', 'application developer', 'aws java geliştirici', 'baş java geliştiricisi', 'bi/ssrs developer', 'business intelligence developer', 'contract career database developer', 'database developer/admin', 'db2 dba & developer', 'dba/developer', 'developer/scrum master', 'devops developer for the database administration team', 'entry-level web developer', 'etl developer', 'exchange developer', 'foxpro programmer', 'freelance sql & database developer', 'full stack developer', 'full stack developer/it', 'full stack java developer', 'full stack java geliştirici', 'full stack java geliştiricisi', 'full stack java/j2ee developer', 'geliştirici', 'hadoop geliştiricisi', 'hadoop/spark geliştiricisi', 'hizmet bilgi geliştirici', 'independent software developer', 'ios developer', 'i̇ş analisti ve rapor geliştiricisi', 'j2ee developer', 'j2ee geliştirici', 'j2ee geliştiricisi', 'j2ee/vitria geliştiricisi', 'java full sstack developer', 'java full stack geliştirici', 'java fullstack geliştirici', 'java geliştirici', 'java geliştirici/üretim desteği', 'java j2ee geliştiricisi', 'java j2se/j2ee developer', 'java programmer', 'java tam yığın geliştiricisi', 'java ui geliştirici', 'java ui geliştiricisi', 'java web developer', 'java çözüm mimarı/java geliştiricisi', 'java ön uç geliştirici', 'java/j2ee developer', 'java/j2ee geliştirici', 'java/j2ee geliştiricisi', 'java/ui developer', 'javaj2ee/ui developer', 'job developer', 'jr. java developer', 'jr. java geliştirici', 'jr. java geliştiricisi', 'jr. sql developer', 'junior database developer', 'junior database developer/report developer', 'junior front-end developer', 'junior ios developer', 'junior java developer', 'kıdemli full stack geliştirici', 'kıdemli geliştirici', 'kıdemli j2ee geliştirici', 'kıdemli j2ee geliştiricisi', 'kıdemli java full stack geliştirici', 'kıdemli java full stack geliştiricisi', 'kıdemli java fullstack geliştirici', 'kıdemli java fullstack geliştiricisi', 'kıdemli java geliştirici', 'kıdemli java geliştirici/mimar', 'kıdemli java geliştiricisi', 'kıdemli java geliştiricisi/mimar', 'kıdemli java geliştiricisi/mimar/güvenlik analisti', 'kıdemli java spring angular geliştirici', 'kıdemli java ui geliştiricisi', 'kıdemli java/hadoop geliştiricisi', 'kıdemli java/j2ee geliştirici', 'kıdemli java/j2ee geliştiricisi', 'kıdemli java/j2ee geliştiricisi/ programcı analizi', 'kıdemli java/j2ee tam yığın geliştirici', 'kıdemli java/ui geliştiricisi', 'kıdemli php baş geliştirici', 'kıdemli php/drupal geliştiricisi', 'kıdemli tam yığın java geliştiricisi', 'lisans access developer', 'mid-level java/j2ee developer', 'mikroservis geliştiricisi', 'mongodb developer', 'ms excel developer', 'ms sql & ssrs developer', 'ms sql server developer', 'obiee developer', 'oracle bi developer', 'oracle d2k developer', 'oracle dba/developer', 'pl/sql/ oracle database developer', 'programmer', 'programmer/system admin', 'reports developer', 'senior analytical hadoop/spark developer', 'senior ios developer', 'senior java developer', 'senior java fullstack developer', 'senior java/hadoop developer', 'senior programmer', 'server-side programmer', 'servicenow developer', 'sharepoint developer', 'sql bi developer/dba', 'sql database developer', 'sql developer', 'sql developer/interim', 'sql developer/programmer', 'sql developer/ssis/ssrs developer', 'sql server developer', 'sql server developer/dba', 'sql/edi programmer', 'sql/etl developer', 'sql/etl geliştiricisi', 'sr java programmer', 'sr. full stack developer', 'sr. full stack java developer', 'sr. full stack java geliştiricisi', 'sr. full stack java web developer', 'sr. j2ee/java developer', 'sr. java developer', 'sr. java full stack developer', 'sr. java full stack geliştirici', 'sr. java geliştirici', 'sr. java j2ee developer', 'sr. java web developer', 'sr. java/hadoop/python developer', 'sr. java/j2ee & web developer', 'sr. java/j2ee developer', 'sr. java/j2ee geliştirici', 'sr. java/python/hadoop developer', 'sr. java/ui developer', 'sr. java/web developer', 'sr. sharepoint developer', 'ssis/raporlar geliştiricisi', 'ssrs developer', 'ssrs/ssis report developer', 'stajyer java geliştiricisi', 'stajyer yazılım geliştiricisi', 'tam yığın java geliştiricisi', 'teknik lider geliştirici', 'ui developer', 'ui/web developer', 'veri tabanı geliştiricisi', 'visual basic developer', 'visual basic programmer', 'web developer', 'web developer/programmer', 'web geliştirici', 'web geliştirici/it destek', 'web geliştiricisi', 'website developer', 'wordpress and drupal developer', 'wordpress geliştiricisi', 'yazılım analisti', 'yazılım programcısı'],
    "Öğretmen": ['adjunct instructor', 'driver trainer/coach', 'eğitim görevlisi / ict eğitmeni', 'graduate student instructor', 'matematik öğretmeni', 'ortaokul bilim öğretmeni', 'public speaking instructor', 'student teacher grades mathematics', 'substitute teacher', 'sunday school teacher', 'swim instructor/lifeguard', 'trainer']    ,
    "Stajyer": ['Stajyer ve Asistan', 'administrative intern', 'adult probation/parole intern', 'araştırma ve i̇letişim stajyeri', 'computer information systems intern', 'eeditoryal stajyer', 'graduate intern', 'i̇çerik oluşturma stajyeri', 'kilise hareketlilikleri stajyeri', 'kiralama yönetimi stajyeri', 'marketing intern', 'proje stajyyeri', 'satış stajyeri', 'security admin intern', 'sosyal medya stajyeri', 'trainee', 'veri talisansnı yönetimi öğrencisi', 'veri yönetim sistemleri stajyer', 'yapım asistanı stajyeri', 'yaz stajyeri', 'yönetim stajyeri', 'öğrenci stajyer'],
    "Teknik Destek ve Sistem Yönetimi": ['crm support', 'inside sales support', 'lab support', 'mysql support dba', 'office support', 'oracle database application support - graduate assistant', 'support associate', 'tech support'],
    "Pazarlama ve Satış": ['Müşteri Hizmetleri ve Satış', 'Müşteri ve Satış Destek', 'Pazarlama ve Dijital Reklam', 'Pazarlama ve İş Geliştirme', 'Perakende ve Toptan Satış', 'Satış ve İş Geliştirme', 'branch sales associate', 'customer service/sales', 'derivatives  sales broker', 'dijital pazarlama müdürü', 'direct sales representative', 'freelance email marketing campaign administration', 'key holder/sales representative', 'outside sales agent', 'satış temsilcisi', 'satış ve müşteri hizmetleri yardımcı müdürü', 'used truck sales', 'çiropraktik asistanı ve pazarlama asistanı'],
    "Danışman": ['Eğitim ve Danışmanlık', 'Eğitim ve Mentorluk', 'baş danışman', 'baş danışman/teknik mimar', 'danışman', 'tekno-fonksiyonel danışman'],
    "Yönetim ve Liderlik": ['kıdemli scrum master', 'oracle dba/scrum master', 'pm / scrum master', 'scrum master/agile coach'],
    "Eğitim ve Araştırma": ['Eğitim ve Destek', 'Eğitim ve Staj', 'Eğitim ve Öğretim', 'araştırma asistanı', 'regional security researcher', 'researcher'],
    "Programcı": ['java geli̇şti̇ri̇ci̇', 'java programcısı', 'java teknik lideri/çözüm mimarı', 'java/j2ee programcısı', 'programcı', 'sistem programcısı', 'yardımcı progr   ramcı'],
    "Geliştirme ve Yazılım": ['oracle database administration / aws solution architecture', 'solution architect/product owner'],


}

# 81 ilin listesi
iller = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", 
    "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", 
    "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", 
    "Gümüşhane", "Hakkari", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", 
    "Karaman", "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", "Kırşehir", "Kilis", "Kocaeli", 
    "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", 
    "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Şanlıurfa", "Şırnak", 
    "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"
]


# "Çalışma Şekli" değerleri
calisma_sekli = ["İş Yerinde", "Hibrit", "Uzaktan"]

# "Çalışma Türü" değerleri
calisma_turu = ["Tam Zamanlı", "Yarı Zamanlı", "Sözleşmeli", "Stajyer"]


# Yeni 'konum' sütunu ekle ve her satıra rastgele bir il ata
df["konum"] = [random.choice(iller) for _ in range(len(df))] 
df["Çalışma Şekli"] = [random.choice(calisma_sekli) for _ in range(len(df))]
df["Çalışma Türü"] = [random.choice(calisma_turu) for _ in range(len(df))]


# 'POZİSYON ADI' sütunundaki pozisyonları düzeltme fonksiyonu
def duzenle_pozisyon_adı(pozisyon_adı):
    if not pozisyon_adı or pd.isna(pozisyon_adı):
        return "Belirtilmemiş"
    
    pozisyon_adı = str(pozisyon_adı).strip().lower()  # Küçük harfe çevir ve baştaki/sondaki boşlukları kaldır
    pozisyon_adı = re.sub(r'\(.*?\)|\(.*', '', pozisyon_adı).strip()  # Parantez içi açıklamaları temizle

    # Eğer pozisyon_adı NaN (yani boş veya eksik) ise, "Belirtilmemiş" döndür
    if pd.isna(pozisyon_adı) or pozisyon_adı == "":
        return "belirtilmemiş"
    
    # Virgüllerine ayırarak işlem yapıyoruz
    pozisyon_adı_listesi = pozisyon_adı.split(',')

    # Her bir pozisyonu eşleştirerek düzeltiyoruz
    duzeltilmis_pozisyonlar = []
    for pozisyon in pozisyon_adı_listesi:
        pozisyon = pozisyon.strip().lower()  # Her bir öğeyi küçük harfe çevir ve boşlukları temizle
        # Eşleştirme sözlüğünü kullanarak her pozisyonu düzeltiyoruz
        matched = False
        for standart_pozisyon, eslesmeler in pozisyon_eslesme.items():
            # Küçük harf farkını gözetmeden eşleşme yap
            if pozisyon in (match.lower().strip() for match in eslesmeler):
                duzeltilmis_pozisyonlar.append(standart_pozisyon)
                matched = True
                break
        # Eğer eşleşme yoksa, orijinal ismi ekle
        if not matched:
            duzeltilmis_pozisyonlar.append(pozisyon)
    
    # Düzeltilmiş pozisyonları tekrar virgülle birleştiriyoruz
    return ','.join(duzeltilmis_pozisyonlar)



yetenek_eslesme={


    }
# 'YETENEKLER' sütunundaki yetenekleri düzeltme
def duzenle_yetenek(yetenek_adı):
    
    if not yetenek_adı or pd.isna(yetenek_adı):
        return "Belirtilmemiş"
    
    yetenek_adı = str(yetenek_adı).strip().lower()  # Küçük harfe çevir ve baştaki/sondaki boşlukları kaldır
    yetenek_adı = re.sub(r'\(.*?\)|\(.*', '', yetenek_adı).strip()  # Parantez içi açıklamaları temizle

    # Eğer yetenek_adı NaN (yani boş veya eksik) ise, "Belirtilmemiş" döndür
    if pd.isna(yetenek_adı) or yetenek_adı == "":
        return "belirtilmemiş"
    
    # Virgüllerine ayırarak işlem yapıyoruz
    yetenek_adı_listesi = yetenek_adı.split(',')

    
    # Her bir kuruluş adı üzerinde işlem yapıyoruz
    duzeltilmis_yetenekler = []
    for yetenek in yetenek_adı_listesi:
        yetenek = yetenek.strip().lower()  # Her bir öğeyi küçük harfe çevir ve boşlukları temizle
        # Eşleştirme sözlüğünü kullanarak her kuruluşu düzeltiyoruz
        for standart_yetenek, eslesmeler in yetenek_eslesme.items():
            # Küçük harf farkını gözetmeden eşleşme yap
            if yetenek in (match.lower().strip() for match in eslesmeler):
                duzeltilmis_yetenekler.append(standart_yetenek)
                break
        else:

            # Eğer eşleşme yoksa, orijinal ismi ekle
            duzeltilmis_yetenekler.append(yetenek)
    
    # Düzeltilmiş kuruluşları tekrar virgülle birleştiriyoruz
    return ','.join(duzeltilmis_yetenekler) 

# 'DİL' sütunundaki dilleri düzeltme
def duzenle_dil(dil_adı):
    dil_adı = str(dil_adı).strip().lower()  # Küçük harfe çevir ve baştaki/sondaki boşlukları kaldır
    dil_adı = re.sub(r'\(.*?\)|\(.*', '', dil_adı).strip()  # Parantez içi açıklamaları temizle

    # Eğer dil_adı NaN (yani boş veya eksik) ise, "Belirtilmemiş" döndür
    if pd.isna(dil_adı) or dil_adı == "":
        return "belirtilmemiş"
    
    # Virgüllerine ayırarak işlem yapıyoruz
    dil_adı_listesi = dil_adı.split(',')

    
    
    # Her bir kuruluş adı üzerinde işlem yapıyoruz
    duzeltilmis_diller = []
    for dil in dil_adı_listesi:
        dil = dil.strip().lower()  # Her bir öğeyi küçük harfe çevir ve boşlukları temizle
        # Eşleştirme sözlüğünü kullanarak her kuruluşu düzeltiyoruz
        for standart_dil, eslesmeler in dil_eslesme.items():
            # Küçük harf farkını gözetmeden eşleşme yap
            if dil in (match.lower().strip() for match in eslesmeler):
                duzeltilmis_diller.append(standart_dil)
                break
        else:

            # Eğer eşleşme yoksa, orijinal ismi ekle
            duzeltilmis_diller.append(dil)
    
    # Düzeltilmiş kuruluşları tekrar virgülle birleştiriyoruz
    return ','.join(duzeltilmis_diller) 

# 'DİL' sütunundaki tüm değerleri düzelt
if 'DİL' in df.columns:
    df['DİL']=df["DİL"].apply(duzenle_dil)

#'POZİSYON ADI" sütunundaki tüm değerleri düzelt 
if 'POZİSYON ADI' in df.columns:
    df['POZİSYON ADI']=df["POZİSYON ADI"].apply(duzenle_pozisyon_adı)

#'YETENEKLER" sütunundaki tüm değerleri düzelt 
if 'YETENEKLER' in df.columns:
    df['YETENEKLER']=df["YETENEKLER"].apply(duzenle_yetenek)

# 'VEREN KURULUŞ' sütunundaki tüm değerleri düzelt
if 'VEREN KURULUŞ' in df.columns:
    df['VEREN KURULUŞ'] = df['VEREN KURULUŞ'].apply(duzenle_kurulus)

if 'BÖLÜM ADI' in df.columns:
    df['BÖLÜM ADI']=df['BÖLÜM ADI'].apply(duzenle_bolum)
    
# Özel sütunlar için 0 ve 1 değerlerini atıyoruz
df = kontrol_ve_guncelle_ozel(df)

# 'DERECE' sütununu işleyerek uygun dereceleri atıyoruz
if 'DERECE' in df.columns:
    df['DERECE'] = df['DERECE'].apply(lambda x: ','.join([replace_degrees(val.strip()) for val in str(x).split(',')]))

# 'MEZUNİYET TARİHİ' sütununda temizlik yapıyoruz
if 'MEZUNİYET TARİHİ' in df.columns:
    df['MEZUNİYET TARİHİ'] = df['MEZUNİYET TARİHİ'].apply(lambda x: ','.join([temizle_tarih(val.strip()) for val in str(x).split(',')]))

    # 'DENEYİM SÜRESİ' sütununu oluşturuyoruz
    df['DENEYİM SÜRESİ'] = df['MEZUNİYET TARİHİ'].apply(deneyim_suresi_hesapla)

# 'BAŞLANGIÇ - BİTİŞ TARİHİ' sütununu temizle
if 'BAŞLANGIÇ - BİTİŞ TARİHİ' in df.columns:
    # Tarihleri temizle
    df['BAŞLANGIÇ - BİTİŞ TARİHİ'] = df['BAŞLANGIÇ - BİTİŞ TARİHİ'].apply(temizle_baslangic_bitis)
    
    # Çalışma zamanlarını hesapla
    df['ÇALIŞMA ZAMANI (YIL)'] = df['BAŞLANGIÇ - BİTİŞ TARİHİ'].apply(calisma_zamani_hesapla)

# 'Unnamed: 17' adlı sütunu siliyoruz
if 'Unnamed: 17' in df.columns:
    df = df.drop(columns=['Unnamed: 17','AD SOYAD','ŞİRKET ADI','ÜNİVERSİTE ADI'])
    
 

# Sütunlardaki değerlerin başındaki ve sonundaki boşlukları temizle ve küçük harfe çevir
df = df.applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)

# Boş (NaN) değerleri 'Belirtilmemiş' ile doldur
df.fillna("belirtilmemiş", inplace=True)

# NaN değerlerini 'Belirtilmemiş' ile değiştir
df = df.replace({pd.NA: "belirtilmemiş", None: "belirtilmemiş", 'nan': 'belirtilmemiş'})

# 'DERECE' sütununu işleyerek uygun dereceleri atıyoruz
if 'DERECE' in df.columns:
    df['DERECE'] = df['DERECE'].replace('belirtilmemiş','')

            
# Sonuçları yeni bir Excel dosyasına kaydetme
output_file = r"C:\Users\beyza\OneDrive\Masaüstü\temizlenmis_cv.xlsx"
df.to_excel(output_file, index=False)