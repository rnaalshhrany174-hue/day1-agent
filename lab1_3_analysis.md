# 📄 المختبر 1.3: وثيقة تحليل بنية الوكيل (Agent Structure Analysis)

### 1. نظرة عامة (Overview)
تستعرض هذه الوثيقة تحليلاً هندسياً لوكيل مساعد الصيانة الأساسي الذي تم تطويره في **المختبر 1.1** (الخيار ب)[span_1](start_span)[span_1](end_span). صُمم الوكيل للتفاعل مع سجلات معدات الصيانة (`maintenance_assets.csv`) عبر الاستعلامات بلغة طبيعية[span_2](start_span)[span_2](end_span)، حيث يقوم بترجمة طلبات المستخدم إلى استدعاءات منظمة للأدوات (`search_assets`) وإعادة معلومات الأصول ذات الصلة مع الاستشهاد بالمصادر[span_3](start_span)[span_3](end_span).

---

### 2. ربط الكود بعناصر الوكيل الأساسية (Mapping Code to Core Agent Elements)
تم ربط العناصر الأربعة الأساسية لهندسة الوكيل بملف `agent.py` بشكل مباشر كالتالي[span_4](start_span)[span_4](end_span):

| عنصر الوكيل | مكان تواجده في ملف `agent.py` | الدور والمفهوم |
| :--- | :--- | :--- |
| **الموجه (Prompt)** | متغير النص `SYSTEM` | يحدد حدود النظام، والشخصية، وقواعد الاستشهاد، وتعليمات المعالجة البديلة[span_5](start_span)[span_5](end_span). |
| **حلقة الوكيل (Agent Loop)** | حلقة التكرار `for _ in range(5)` داخل `run_agent()` | تنفذ دورة (التخطيط ← التنفيذ ← المراقبة) الذاتية حتى الحد الأقصى لخطوات التكرار[span_6](start_span)[span_6](end_span). |
| **واجهة الأدوات (Tool Interface)** | مخطط `TOOLS` + دالة `search_assets()` | تنسيق وتنفيذ قدرات استدعاء الدوال (Function Calling) على بيانات ملف الـ CSV المحلي[span_7](start_span)[span_7](end_span). |
| **الذاكرة (Memory)** | قائمة `messages` | تعمل كحِساء سياقي قصير المدى لتتبع المحادثات ونتائج استدعاء الأدوات[span_8](start_span)[span_8](end_span). |

---

### 3. المتطلبات الوظيفية (Functional Requirements)
* **FR-1:** يجب على الوكيل تحليل أسئلة المستخدم المتعلقة بمعدات المصنع واستخراج معاملات البحث المنظمة (الحالة، مستوى الأهمية، نوع الأصل، الموقع)[span_9](start_span)[span_9](end_span).
* **FR-2:** يجب على الوكيل استدعاء أداة `search_assets` بالمعاملات المناسبة عندما يتطلب الأمر استرجاع معلومات من قاعدة البيانات[span_10](start_span)[span_10](end_span).
* **FR-3:** يجب على الوكيل ذكر معرّفات الأصول (`asset_id`) المحددة في كل رد يحتوي على تفاصيل المعدات[span_11](start_span)[span_11](end_span).
* **FR-4:** يجب على الوكيل توضيح الأمر بوضوح عندما لا توجد السجلات المطلوبة أو معلومات المعدات في مجموعة البيانات[span_12](start_span)[span_12](end_span).
* **FR-5:** يجب على الوكيل الحفاظ على سياق المحادثة ونتائج الأدوات داخل ذاكرة مؤقتة قصيرة المدى (قائمة `messages`)[span_13](start_span)[span_13](end_span).
* **FR-6:** يجب على الوكيل تقييد تنفيذ الحلقة الذاتية بحد أقصى يبلغ 5 تكرارات لمنع الحلقات اللانهائية[span_14](start_span)[span_14](end_span).

---

### 4. مخطط المكونات (Component Diagram)

```plantuml
@startuml
skinparam componentStyle uml2

actor المستخدم as User
package "هندسة الوكيل الأساسي" {
    component "واجهة المستخدم (CLI)" as UI
    component "حلقة الوكيل\n(run_agent)" as Loop
    component "الموجه النظامي (Prompt)" as Prompt
    component "واجهة نموذج اللغة\n(OpenAI / OpenRouter)" as Model
    component "واجهة الأدوات\n(search_assets)" as Tools
    database "الذاكرة\n(قائمة messages)" as Mem
    database "ملف سجلات الأصول CSV\n(maintenance_assets.csv)" as DB
}

User --> UI : 1. إرسال الاستعلام
UI --> Loop : 2. بدء المهمة
Loop --> Prompt : 3. تحميل قواعد النظام
Loop --> Mem : 4. إلحاق السياق
Loop --> Model : 5. إرسال الموجه + الأدوات + السجل
Model --> Loop : 6. إرجاع التفكير / أمر الأداة
Loop --> Tools : 7. تنفيذ استدعاء الأداة
Tools --> DB : 8. الاستعلام عن سجلات الأصول
DB --> Tools : 9. إرجاع الصفوف المتطابقة
Tools --> Loop : 10. تغذية راجعة للملاحظة
Loop --> Mem : 11. إلحاق نتيجة الأداة
Loop --> UI : 12. تقديم الإجابة النهائية
@enduml