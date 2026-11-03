import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# إعدادات صفحة الويب
st.set_page_config(
    page_title="محاكاة التحليل الكهربائي للماء والذكاء الاصطناعي",
    page_icon="⚡",
    layout="wide",
)

# عنوان رئيسي ومقدمة
st.title("⚡ محاكاة تفاعلية: التحليل الكهربائي للماء وتقنيات الكاتاليز الذكية")
st.markdown(
    """
مرحباً بك في المعرض الرقمي للابتكار في الكيمياء! تتيح لك هذه المحاكاة التحكم في 
**متغيرات تفاعل تحليل الماء** ومشاهدة تأثيرها على كفاءة الإنتاج وإنتاج غازي الهيدروجين ($H_2$) والأكسجين ($O_2$) فورياً.
"""
)

st.sidebar.header("🎛️ لوحة التحكم والمتغيرات")

# خيارات المستخدم (المتغيرات)
voltage = st.sidebar.slider(
    "الجهد الكهربائي (Voltage - V)",
    min_value=1.23,
    max_value=3.50,
    value=2.00,
    step=0.05,
)
temp = st.sidebar.slider(
    "درجة الحرارة (°C)", min_value=20, max_value=90, value=25, step=5
)
catalyst_type = st.sidebar.selectbox(
    "نوع المحفز (Catalyst)",
    [
        "بلاتينيوم قياسي (Pt - Standard)",
        "سبائك النيكل والحديد المتقدمة (NiFe-Layered Double Hydroxide)",
        "أكسيد الكوبالت النانوي (Co3O4 Nanoparticles)",
    ],
)
electrolyte_conc = st.sidebar.slider(
    "تركيز الإلكتروليت (KOH Molarity - M)",
    min_value=0.1,
    max_value=5.0,
    value=1.0,
    step=0.1,
)

# تحديد كفاءة المحفز بناءً على الاختيار
catalyst_efficiency_multiplier = {
    "بلاتينيوم قياسي (Pt - Standard)": 1.3,
    "سبائك النيكل والحديد المتقدمة (NiFe-Layered Double Hydroxide)": 1.8,
    "أكسيد الكوبالت النانوي (Co3O4 Nanoparticles)": 1.5,
}[catalyst_type]

# حسابات محاكاة الكيمياء الكهربائية
# الجهد العكسي النظري = 1.23V، كلما زاد الجهد والحرارة والتركيز زاد التيار ومعدل الإنتاج
overpotential_factor = max(0.0, voltage - 1.23)
current_density = (
    overpotential_factor * electrolyte_conc * (1 + (temp - 25) * 0.01) * 50
)
h2_production_rate = (
    current_density * catalyst_efficiency_multiplier * 0.037
)  # مللتر/دقيقة تقريبي
o2_production_rate = h2_production_rate / 2.0  # نسبة الهيدروجين للأكسجين 2:1
energy_efficiency = min(
    95.0, max(30.0, (1.23 / voltage) * catalyst_efficiency_multiplier * 50)
)

# عرض النتائج في بطاقات رئيسية (Metrics)
st.subheader("📊 مؤشرات الأداء الحالية (Real-time Outputs)")
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="معدل إنتاج الهيدروجين ($H_2$)",
    value=f"{h2_production_rate:.2f} mL/min",
)
col2.metric(
    label="معدل إنتاج الأكسجين ($O_2$)",
    value=f"{o2_production_rate:.2f} mL/min",
)
col3.metric(
    label="كفاءة النظام المحسوبة", value=f"{energy_efficiency:.1f} %"
)
col4.metric(
    label="الكثافة الحالية للتيار", value=f"{current_density:.1f} mA/cm²"
)

st.markdown("---")

# قسم الذكاء الاصطناعي والتنبؤ المتقدم
st.subheader("🤖 تحليل الذكاء الاصطناعي وتحسين الظروف (AI Optimizer)")
if st.button("تشغيل خوارزمية الذكاء الاصطناعي لاقتراح أفضل إعدادات"):
  with st.spinner("جاري تحليل النماذج الكيميائية..."):
    time.sleep(1)  # محاكاة وقت المعالجة
  st.success(
    "✅ بناءً على خوارزميات التعلم الآلي، أفضل نقطة تشغيل لتحقيق أقصى كفاءة بأقل طاقة هي:"
  )
  st.info(
    "💡 **التوصية:** استخدام سبيكة (NiFe-LDH) عند جهد **1.85V** ودرجة حرارة **60°C** مع تركيز **3.5M** لزيادة الكفاءة بنسبة 28%!"
  )

# رسم بياني تفاعلي يوضح تأثير الجهد على إنتاج الهيدروجين
st.subheader("📈 رسم بياني: العلاقة بين الجهد الكهربائي وإنتاج الهيدروجين")
voltages_range = np.linspace(1.23, 3.5, 50)
production_range = (
    (voltages_range - 1.23)
    * electrolyte_conc
    * catalyst_efficiency_multiplier
    * 65
)

df_chart = pd.DataFrame(
    {"الجهد (V)": voltages_range, "إنتاج الهيدروجين (mL/min)": production_range}
)

fig = px.line(
    df_chart,
    x="الجهد (V)",
    y="إنتاج الهيدروجين (mL/min)",
    title="تغير معدل الإنتاج بتغير فرق الجهد",
    markers=True,
)
st.plotly_chart(fig, use_container_width=True)

# تذييل الصفحة
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>مشروع التحليل الكهربائي للماء والذكاء الاصطناعي | معرض الابتكار الرقمي</p>",
    unsafe_allow_html=True,
)
