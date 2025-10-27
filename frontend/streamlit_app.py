"""
Streamlit Chat Interface - 100% LOCAL
No external APIs required
"""
import streamlit as st
import requests
from typing import List, Dict
import time

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Property Search Chatbot - LOCAL",
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
.local-badge {
    background-color: #dcfce7;
    color: #166534;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
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
    '<span class="local-badge">✓ 100% LOCAL - No API Keys Required</span><br>'
    'Ask me about properties like: <i>"3BHK flat in Pune under ₹1.2 Cr"</i>'
    '</div>', 
    unsafe_allow_html=True
)

# Sidebar with examples
with st.sidebar:
    st.header("📝 Example Queries")
    example_queries = [
        "3BHK flat in Pune under ₹1.2 Cr",
        "2BHK ready to move in Mumbai",
        "Properties in Bangalore under 80 lakhs",
        "4BHK apartments near Baner",
        "Show me 1BHK under construction",
    ]
    
    st.write("Click to try:")
    for example in example_queries:
        if st.button(example, key=example):
            st.session_state.query_input = example
    
    st.divider()
    st.info("🚀 **Fully LOCAL Processing**\n\n"
            "✓ No OpenAI API\n\n"
            "✓ No external services\n\n"
            "✓ Runs on your machine\n\n"
            "✓ CSV-based search")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if "properties" in message and message["properties"]:
            for prop in message["properties"]:
                status_class = "status-ready" if "ready" in prop['possession_status'].lower() else "status-construction"
                
                amenities_html = "".join([f'<span class="badge">{amenity}</span>' for amenity in prop['amenities']])
                
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
                        <strong>✨ Amenities:</strong> {amenities_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask about properties..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching properties locally..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/chat",
                    json={"message": prompt},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display summary
                    st.markdown(f"**{data['summary']}**")
                    
                    # Display properties
                    if data['properties']:
                        st.markdown(f"---")
                        for prop in data['properties']:
                            status_class = "status-ready" if "ready" in prop['possession_status'].lower() else "status-construction"
                            amenities_html = "".join([f'<span class="badge">{amenity}</span>' for amenity in prop['amenities']])
                            
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
                                    <strong>✨ Amenities:</strong> {amenities_html}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No properties found matching your criteria. Try adjusting your filters!")
                    
                    # Save assistant message
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data['summary'],
                        "properties": data['properties']
                    })
                else:
                    st.error(f"❌ Failed to get response from server (Status: {response.status_code})")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Please ensure the FastAPI server is running:\n\n"
                        "``````")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
