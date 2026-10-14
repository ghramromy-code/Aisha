import streamlit as st
from PIL import Image, ImageDraw
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="مبادرة عالم العلوم - ابتدائية الوقبة",
    page_icon="🌸",
    layout="centered"
)

# --- 2. إضافة الأنميشن والتصميم الوردي البناتي خلف الكلام باستخدام CSS ---
st.markdown("""
    <style>
    /* خلفية التطبيق الداكنة البنفسجية مع الأنميشن */
    .stApp {
        background: linear-gradient(180deg, #1A0B2E 0%, #2D1B4E 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        overflow-x: hidden;
    }

    /* كروت الهيدر والأسئلة شفافة تظهر الحركة وراءها */
    .header-box {
        background: linear-gradient(135deg, #FF6B9B 0%, #C850C0 50%, #4158D0 100%);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        margin-bottom: 25px;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    .header-title { font-size: 24px; font-weight: bold; margin-bottom: 5px; }
    .header-sub { font-size: 20px; color: #FFE500; font-weight: bold; margin-bottom: 5px; }
    .header-teacher { font-size: 15px; color: #FFFFFF; opacity: 0.9; }

    /* أنميشن الكائنات والحيوانات الطائرة خلف الكلام */
    @keyframes float {
        0% { transform: translateY(100vh) rotate(0deg) scale(0.8); opacity: 0; }
        20% { opacity: 0.8; }
        80% { opacity: 0.8; }
        100% { transform: translateY(-10vh) rotate(360deg) scale(1.2); opacity: 0; }
    }

    .floating-icon {
        position: fixed;
        z-index: 0;
        font-size: 32px;
        pointer-events: none;
        animation: float 10s linear infinite;
    }

    /* مواقع ومواعيد ظهور الحيوانات المتحركة */
    .icon1 { left: 8%; animation-duration: 8s; animation-delay: 0s; }
    .icon2 { left: 25%; animation-duration: 12s; animation-delay: 2s; font-size: 40px; }
    .icon3 { left: 48%; animation-duration: 9s; animation-delay: 4s; }
    .icon4 { left: 70%; animation-duration: 11s; animation-delay: 1s; font-size: 36px; }
    .icon5 { left: 88%; animation-duration: 10s; animation-delay: 3s; }

    /* أزرار ملونة كبيرة تناسب البنات */
    .stButton > button {
        width: 100%;
        border-radius: 18px !important;
        height: 60px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        color: white !important;
        background: linear-gradient(90deg, #FF4081 0%, #FF6B9B 100%) !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
        transition: transform 0.2s !important;
    }
    .stButton > button:hover { transform: scale(1.03); }

    /* تحسين خيارات الإجابة والنصوص */
    h1, h2, h3, h4, p, label { color: white !important; text-align: center; }
    
    /* إخفاء قوائم ستريمليت الإضافية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    <!-- الأشكال والحيوانات المتحركة في الخلفية -->
    <div class="floating-icon icon1">🦋</div>
    <div class="floating-icon icon2">🌸</div>
    <div class="floating-icon icon3">🐰</div>
    <div class="floating-icon icon4">🌿</div>
    <div class="floating-icon icon5">🐥</div>
""", unsafe_allow_html=True)

# --- 3. إدارة حالة التطبيق ---
if 'level' not in st.session_state:
    st.session_state.level = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""

# --- 4. الهيدر العالي والمترتب ---
st.markdown("""
    <div class="header-box">
        <div class="header-title">ابتدائية الوقبة</div>
        <div class="header-sub">مبادرة عالم العلوم 🌿</div>
        <div class="header-teacher">إعداد وتجميع: أ. عائشة العمر</div>
        <div class="header-teacher">مديرة المدرسة: أ. سالمة العمري</div>
    </div>
""", unsafe_allow_html=True)

# --- 5. بنك الأسئلة (المستويات) ---
questions_db = {
    1: [
        {"q": "أي مما يلي يُعتبر من الكائنات الحية؟", "options": ["الحجر", "النبات", "السيارة"], "answer": "النبات"},
        {"q": "ماذا تحتاج النبتة الجميلة لتصنع غذاءها؟", "options": ["ضوء الشمس والماء", "الحليب والعصير", "الألعاب"], "answer": "ضوء الشمس والماء"},
        {"q": "الجزء الذي يمتص الماء من التربة هو:", "options": ["الأوراق", "الأزهار", "الجذور"], "answer": "الجذور"}
    ],
    2: [
        {"q": "الحيوانات التي تأكل الأعشاب والنباتات فقط تسمى:", "options": ["أكلات لحوم", "أكلات أعشاب", "قارضة"], "answer": "أكلات أعشاب"}
    ]
}

# --- 6. الشاشات والتفاعل ---
if not st.session_state.student_name:
    st.markdown("### 🌸 أهلاً بكِ يا بطلة المستقبل 🌸")
    name_input = st.text_input("أدخلي اسمكِ الثلاثي المبدع للبدء:")
    if st.button("ابدأي المغامرة 🚀"):
        if name_input:
            st.session_state.student_name = name_input
            st.rerun()

elif st.session_state.level == 0:
    st.markdown(f"### أهلاً بكِ يا فراشة العلوم: **{st.session_state.student_name}** 🦋")
    st.markdown("#### اختاري مستواكِ وابدأي التحدي! 🎒")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("المستوى الأول 🌸"):
            st.session_state.level = 1
            st.rerun()
        if st.button("المستوى الثالث 🌿"):
            st.session_state.level = 3
            st.rerun()
        if st.button("المستوى الخامس 👑"):
            st.session_state.level = 5
            st.rerun()
            
    with col2:
        if st.button("المستوى الثاني 🌺"):
            st.session_state.level = 2
            st.rerun()
        if st.button("المستوى الرابع 🦋"):
            st.session_state.level = 4
            st.rerun()
        if st.button("المستوى السادس 🏆"):
            st.session_state.level = 6
            st.rerun()

else:
    current_level = st.session_state.level
    if current_level in questions_db:
        questions = questions_db[current_level]
        q_idx = st.session_state.current_q
        
        if q_idx < len(questions):
            st.markdown(f"### المستوى {current_level} — السؤال ({q_idx + 1}/{len(questions)})")
            q_data = questions[q_idx]
            
            st.info(q_data["q"])
            selected_option = st.radio("اختاري الإجابة الصحيحة:", q_data['options'], key=f"q_{current_level}_{q_idx}")
            
            if st.button("إرسال الإجابة 🎯"):
                if selected_option == q_data['answer']:
                    st.success("إجابة صحيحة وممتازة! أحسنتِ يا مبدعة! 🎉")
                    st.session_state.score += 1
                else:
                    st.error(f"حاولي مرة أخرى! الإجابة الصحيحة هي: {q_data['answer']}")
                
                st.session_state.current_q += 1
                st.rerun()
        else:
            st.balloons()
            st.success(f"🏆 رائعة جداً! أكملتِ المستوى {current_level} بنجاح!")
            if st.button("العودة لشاشة المستويات ➡️"):
                st.session_state.level = 0
                st.session_state.current_q = 0
                st.rerun()
    else:
        st.info("هذا المستوى سيتم فتحه قريباً!")
        if st.button("رجوع"):
            st.session_state.level = 0
            st.rerun()
            # إخفاء شريط GitHub العلوي والتذييل السلفي بالكامل
st.markdown("""
    <style>
    /* إخفاء القائمة والشريط العلوي (GitHub/Fork) */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* إخفاء شريط Created by و Streamlit الأسفل */
    .stApp > header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    div[class^="viewerBadge"] {display: none !important;}
    footer {display: none !important;}
    </style>
""", unsafe_allow_html=True)
