# مول الحسن - مبنى الحسن السياحي (Al Hasan Mall Digital Hub)
### حدائق أكتوبر، محافظة الجيزة، مصر | October Gardens, Giza, Egypt

منصة الويب والتطبيق التجاري الرقمي المتكامل لـ **مول الحسن (مبنى الحسن السياحي)**، أحد صروح مجموعة ماهر حسن للتنمية العمرانية، الواقع في منطقة 247 عمارة (حي الكوثر) على شارع زويل الرئيسي أمام جهاز مدينة حدائق أكتوبر.

---

## 🏛️ هيكل المشروع (Project Architecture)

```text
moll al hassan2/
├── backend/
│   ├── __init__.py      # حزمة بايثون الخلفية
│   ├── database.py      # إعداد SQLAlchemy وقاعدة بيانات SQLite
│   ├── models.py        # نماذج الجداول (Store و Inquiry)
│   ├── schemas.py       # مخططات التحقق Pydantic v2
│   └── main.py          # تطبيق FastAPI، معالجة CORS، التعبئة التلقائية وتخديم الواجهة
├── frontend/
│   ├── index.html       # الواجهة التفاعلية الفاخرة (Tailwind + Lucide + Arabic RTL)
│   └── assets/
│       └── logo.jpg     # الشعار المعماري الرسمي لمول الحسن
├── requirements.txt     # مكتبات بايثون المطلوبة
└── README.md            # دليل التشغيل والنشر
```

---

## 🚀 التشغيل المحلي (Local Development)

### 1. إعداد البيئة الافتراضية وتثبيت الاعتمادات
```bash
# إنشاء بيئة بايثون افتراضية (اختياري لكن مفضل)
python -m venv venv

# تفعيل البيئة (ويندوز)
.\venv\Scripts\activate

# تفعيل البيئة (لينكس / ماك)
source venv/bin/activate

# تثبيت متطلبات المشروع
pip install -r requirements.txt
```

### 2. تشغيل السيرفر المحلي
```bash
uvicorn backend.main:app --reload --port 8000
```

* **الواجهة الأمامية (SPA):** افتح المتصفح على [http://localhost:8000](http://localhost:8000)
* **توثيق الـ API التفاعلي (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **توثيق ReDoc البديل:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

> **ملاحظة:** عند تشغيل التطبيق لأول مرة، يقوم النظام تلقائياً بتوليد قاعدة بيانات `mall.db` وإدراج **كافة المحلات والأنشطة الحقيقية الـ 23 لمول الحسن (Auto-Seeding)**.

---

## 📡 نقاط الاتصال البرمجية (REST API Endpoints)

| المسار (Endpoint) | الطريقة (Method) | الوصف | الحماية |
|---|---|---|---|
| `/` | `GET` | تخديم الواجهة الأمامية الرئيسية | عام |
| `/api/stores` | `GET` | استرجاع قائمة كافة متاجر وخدمات المول | عام |
| `/api/stores` | `POST` | إضافة متجر جديد لقاعدة البيانات | يتطلب هيدر `X-Admin-Key` |
| `/api/stores/{id}` | `DELETE` | حذف متجر من الدليل | يتطلب هيدر `X-Admin-Key` |
| `/api/inquiries` | `POST` | تسجيل طلب تأجير أو استفسار استثماري جديد | عام |
| `/api/inquiries` | `GET` | استعراض كافة طلبات التأجير مرتبة بالأحدث | يتطلب هيدر `X-Admin-Key` |

### المتغيرات البيئية ومفتاح الإدارة (Admin Security)
* الافتراضي: `ADMIN_KEY="hasan2026"`
* يمكنك تخصيصه بتعيين متغير بيئي: `export ADMIN_KEY="your_secure_password"`

#### مثال إضافة متجر عبر cURL:
```bash
curl -X POST "http://localhost:8000/api/stores" \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: hasan2026" \
  -d '{
    "name": "محل تجريبي جديد",
    "cat": "r",
    "phone": "01000000000",
    "open24": false
  }'
```

#### رموز التصنيفات المعتمدة (`cat`):
* `r`: مطاعم وكافيهات (Restaurants & Cafes)
* `m`: سوبر ماركت وتموين وأغذية (Supermarket & Food)
* `s`: صيانة وتشطيبات وبويات (Supplies & Finishing)
* `h`: خدمات طبية وصيدليات وعيادات (Health & Clinics)
* `f`: رياضة ولياقة وعناية شخصية (Fitness & Grooming)
* `g`: مكتبات وهدايا ومنظفات (Gifts & Stationery)

---

## ☁️ دليل النشر السحابي (Deployment)

### النشر على منصة Render
1. أنشئ حساباً على [Render.com](https://render.com) واربط مستودع GitHub الخاص بالمشروع.
2. اختر **New Web Service**.
3. حدد الإعدادات التالية:
   * **Runtime:** `Python 3`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:**
     ```bash
     uvicorn backend.main:app --host 0.0.0.0 --port $PORT
     ```
4. أضف المتغيرات البيئية (Environment Variables):
   * `ADMIN_KEY`: كلمة مرور آمنة للوحة الإدارة.

### النشر على منصة Railway
1. اختر **Deploy from GitHub repo**.
2. سيقوم Railway باكتشاف ملف `requirements.txt` تلقائياً.
3. اضبط أمر التشغيل (Custom Start Command):
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```

---

## 🏢 حقوق الملكية الفكرية
جميع الحقوق محفوظة © **مول الحسن (مبنى الحسن السياحي)** - أحد مشاريع **مجموعة ماهر حسن للتنمية العمرانية** 2026.
حدائق أكتوبر - شارع زويل الرئيسي أمام جهاز المدينة.
هاتف الإدارة: `01023876666`

