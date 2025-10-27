"""
Property Search Chatbot - Streamlit Interface
"""
import streamlit as st
import requests
import os
from typing import List, Dict

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Property Search Chatbot",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 42px;
    font-weight: bold;
    color: #1e3a8a;
    text-align: center;
    margin-bottom: 10px;
}
.sub-header {
    text-align: center;
    color: #64748b;
    margin-bottom: 30px;
    font-size: 16px;
}
.property-card {
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}
.property-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.property-title {
    font-size: 22px;
    font-weight: bold;
    color: #1e293b;
    margin-bottom: 8px;
}
.property-price {
    font-size: 24px;
    color: #16a34a;
    font-weight: bold;
    margin: 10px 0;
}
.property-details {
    color: #475569;
    font-size: 15px;
    line-height: 1.6;
}
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    background-color: #dbeafe;
    color: #1e40af;
    font-size: 13px;
    margin: 4px 4px 4px 0;
}
.status-ready {
    background-color: #d1fae5;
    color: #065f46;
}
.status-construction {
    background-color: #fed7aa;
    color: #92400e;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown('<div class="main-header">🏠 Property Search Chatbot</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">'
    'Find your dream property with natural language search. '
    'Try: <i>"3BHK flat in Pune under ₹1.2 Cr"</i>'
    '</div>', 
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("📝 Example Searches")
    
    st.markdown("Try Typing This Example")
    
    example_queries = [
        "3BHK flat in Pune under ₹1.2 Cr",
        "2BHK ready to move in Mumbai",
        "Properties under 80 lakhs",
        "4BHK apartments near Baner",
        "1BHK under construction in Pune",
        "Ready to move properties in Bangalore"
    ]
    
    for example in example_queries:
        if st.button(example, key=example, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": example})
            st.rerun()
    
    st.divider()
    
    st.subheader("🎯 Features")
    st.markdown("""
    - Natural language understanding
    - Smart filter extraction
    - Real-time property search
    - Detailed property cards
    - Budget-based filtering
    - Location-based search
    """)
    
    st.divider()
    
    st.subheader("ℹ️ How to Use")
    st.markdown("""
    1. Type your property requirements naturally
    2. Mention city, BHK, budget, or status
    3. Get instant results with summaries
    4. View detailed property cards
    """)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if "properties" in message and message["properties"]:
            st.markdown("---")
            
            prop_count = len(message["properties"])
            st.markdown(f"**Found {prop_count} {'property' if prop_count == 1 else 'properties'}**")
            
            for prop in message["properties"]:
                status_class = "status-ready" if "ready" in prop['possession_status'].lower() else "status-construction"
                
                amenities_html = "".join([
                    f'<span class="badge">{amenity}</span>' 
                    for amenity in prop['amenities']
                ])
                
                st.markdown(f"""
                <div class="property-card">
                    <div class="property-title">🏢 {prop['title']}</div>
                    <div class="property-price">{prop['price']}</div>
                    <div class="property-details">
                        <strong>📍 Location:</strong> {prop['locality']}, {prop['city']}<br>
                        <strong>🏠 Configuration:</strong> {prop['bhk']}<br>
                        <strong>📅 Status:</strong> <span class="badge {status_class}">{prop['possession_status']}</span><br>
                        {f"<strong>📐 Carpet Area:</strong> {prop['carpet_area']:.0f} sq.ft<br>" if prop.get('carpet_area') else ''}
                        {f"<strong>🚿 Bathrooms:</strong> {prop['bathrooms']}<br>" if prop.get('bathrooms') else ''}
                        {f"<strong>🏞️ Balconies:</strong> {prop['balconies']}<br>" if prop.get('balconies') else ''}
                        <strong>✨ Amenities:</strong> {amenities_html if amenities_html else 'Contact for details'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Describe your property requirements..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching properties..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/chat",
                    json={"message": prompt},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.markdown(f"**{data['summary']}**")
                    
                    if data['properties']:
                        st.markdown("---")
                        
                        prop_count = len(data['properties'])
                        st.markdown(f"**Found {prop_count} {'property' if prop_count == 1 else 'properties'}**")
                        
                        for prop in data['properties']:
                            status_class = "status-ready" if "ready" in prop['possession_status'].lower() else "status-construction"
                            
                            amenities_html = "".join([
                                f'<span class="badge">{amenity}</span>' 
                                for amenity in prop['amenities']
                            ])
                            
                            st.markdown(f"""
                            <div class="property-card">
                                <div class="property-title">🏢 {prop['title']}</div>
                                <div class="property-price">{prop['price']}</div>
                                <div class="property-details">
                                    <strong>📍 Location:</strong> {prop['locality']}, {prop['city']}<br>
                                    <strong>🏠 Configuration:</strong> {prop['bhk']}<br>
                                    <strong>📅 Status:</strong> <span class="badge {status_class}">{prop['possession_status']}</span><br>
                                    {f"<strong>📐 Carpet Area:</strong> {prop['carpet_area']:.0f} sq.ft<br>" if prop.get('carpet_area') else ''}
                                    {f"<strong>🚿 Bathrooms:</strong> {prop['bathrooms']}<br>" if prop.get('bathrooms') else ''}
                                    {f"<strong>🏞️ Balconies:</strong> {prop['balconies']}<br>" if prop.get('balconies') else ''}
                                    <strong>✨ Amenities:</strong> {amenities_html if amenities_html else 'Contact for details'}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("💡 No properties found matching your criteria. Try adjusting your budget or location preferences.")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data['summary'],
                        "properties": data['properties']
                    })
                else:
                    st.error(f"⚠️ Server returned status code: {response.status_code}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to the backend API.")
                st.info("Please ensure the backend is running at `http://localhost:8000`")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🏠 Property Search Bot**")
    st.caption("Made By Jayesh Salunke GitHub@JayeshSalunkeAI")

with col2:
    st.markdown("**📊 Search Capabilities**")
    st.caption("City • BHK • Budget • Status")

with col3:
    st.markdown("**🔧 Tech Stack**")
    st.caption("Python • FastAPI • Streamlit")

