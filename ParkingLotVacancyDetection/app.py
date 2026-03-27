"""
Parking Space Detection - Multi-Slot Analysis
Upload a parking lot image to detect and count vacant/occupied spaces
"""

import streamlit as st
import cv2
import numpy as np
from pathlib import Path
import torch
from PIL import Image
import json

# Set page config
st.set_page_config(
    page_title="Parking Lot Analyzer",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem;
    }
    .stat-occupied { color: #d32f2f; font-size: 2em; font-weight: bold; }
    .stat-vacant { color: #388e3c; font-size: 2em; font-weight: bold; }
    .stat-total { color: #1976d2; font-size: 2em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
    <h1>🅿️ Parking Lot Analyzer</h1>
    <p>Upload a parking lot image to analyze all spaces and get occupancy statistics</p>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
    st.session_state.clf = None
if 'slots' not in st.session_state:
    st.session_state.slots = []
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

device = st.sidebar.selectbox(
    "Processing Device",
    options=["CPU", "GPU (CUDA)"],
    help="GPU requires NVIDIA CUDA installed"
)
device_str = "cuda" if device == "GPU (CUDA)" else "cpu"

conf_threshold = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05,
    help="Higher = stricter classification"
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔧 Slot Detection")

slot_detection_method = st.sidebar.radio(
    "How to define parking slots:",
    options=["Auto-Grid (Recommended)", "Upload Config", "Manual Grid"],
    help="Choose how to detect parking spaces"
)

# Load model
@st.cache_resource
def load_model(device_type, conf_thresh):
    """Load the trained ResNet model"""
    from module4_deep_learning.inference_engine import ResNetClassifier
    model = ResNetClassifier(
        weights_path='module4_deep_learning/resnet18_parking.pth',
        device=device_type,
        conf_threshold=conf_thresh
    )
    return model

if st.sidebar.button("🔄 Load Model", use_container_width=True):
    try:
        with st.spinner('Loading trained ResNet18 model...'):
            st.session_state.clf = load_model(device_str, conf_threshold)
            st.session_state.model_loaded = True
            st.sidebar.success("✅ Model loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"❌ Error loading model: {str(e)}")

if st.session_state.model_loaded:
    st.sidebar.info(f"✅ Model Ready\n\nDevice: {device_str.upper()}\nThreshold: {conf_threshold}")
else:
    st.sidebar.warning("⚠️ Click 'Load Model' to start")

# Main content
st.header("📸 Upload Parking Lot Image")

uploaded_file = st.file_uploader(
    "Choose a parking lot image",
    type=["jpg", "jpeg", "png", "bmp"],
    help="Upload an aerial or high-angle view of your parking lot"
)

if uploaded_file and st.session_state.model_loaded:
    try:
        # Read image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        
        # Display uploaded image
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image(image_rgb, caption="Uploaded Parking Lot Image", use_column_width=True)
        
        # Slot detection setup
        with col2:
            st.subheader("🎯 Slot Setup")
            
            if slot_detection_method == "Auto-Grid (Recommended)":
                st.markdown("**Auto-detect parking spaces in a grid:**")
                grid_rows = st.number_input("Rows", min_value=1, max_value=20, value=5)
                grid_cols = st.number_input("Columns", min_value=1, max_value=30, value=8)
                st.info(f"Will detect {grid_rows * grid_cols} parking spaces")
                
                if st.button("🔍 Detect Slots (Grid)", key="grid_btn", use_container_width=True):
                    with st.spinner("Generating grid layout..."):
                        h, w = image_rgb.shape[:2]
                        slot_h = h // grid_rows
                        slot_w = w // grid_cols
                        
                        st.session_state.slots = []
                        for row in range(grid_rows):
                            for col in range(grid_cols):
                                slot = {
                                    'id': len(st.session_state.slots),
                                    'x': col * slot_w,
                                    'y': row * slot_h,
                                    'w': slot_w,
                                    'h': slot_h,
                                    'label': f"{chr(65+row)}{col+1}"
                                }
                                st.session_state.slots.append(slot)
                        st.success(f"✓ Generated {len(st.session_state.slots)} slots")
            
            elif slot_detection_method == "Upload Config":
                config_file = st.file_uploader("Upload slots_config.json", type=['json'], key="config_uploader")
                if config_file and st.button("📤 Load Config", use_container_width=True):
                    try:
                        config_data = json.load(config_file)
                        st.session_state.slots = config_data.get('slots', [])
                        st.success(f"✓ Loaded {len(st.session_state.slots)} slots")
                    except Exception as e:
                        st.error(f"Error loading config: {e}")
            
            elif slot_detection_method == "Manual Grid":
                st.markdown("**Define grid manually:**")
                start_x = st.number_input("Start X", value=0, min_value=0)
                start_y = st.number_input("Start Y", value=0, min_value=0)
                slot_width = st.number_input("Slot Width", value=100, min_value=10)
                slot_height = st.number_input("Slot Height", value=100, min_value=10)
                rows = st.number_input("Rows", value=5, min_value=1, max_value=20)
                cols = st.number_input("Columns", value=8, min_value=1, max_value=30)
                
                if st.button("✏️ Create Grid", use_container_width=True):
                    st.session_state.slots = []
                    for row in range(rows):
                        for col in range(cols):
                            slot = {
                                'id': len(st.session_state.slots),
                                'x': start_x + col * slot_width,
                                'y': start_y + row * slot_height,
                                'w': slot_width,
                                'h': slot_height,
                                'label': f"{chr(65+row)}{col+1}"
                            }
                            st.session_state.slots.append(slot)
                    st.success(f"✓ Created {len(st.session_state.slots)} slots")
        
        # Analyze if slots are defined
        if st.session_state.slots and st.button("🎯 Analyze All Slots", use_container_width=True):
            with st.spinner("🤖 Analyzing parking lot..."):
                results = []
                
                for slot in st.session_state.slots:
                    x, y, w, h = slot['x'], slot['y'], slot['w'], slot['h']
                    
                    # Extract slot region with bounds checking
                    y_end = min(y+h, image_bgr.shape[0])
                    x_end = min(x+w, image_bgr.shape[1])
                    
                    if y_end <= y or x_end <= x:
                        continue
                    
                    slot_region = image_bgr[y:y_end, x:x_end]
                    if slot_region.size == 0:
                        continue
                    
                    # Resize to 64x64 for model
                    slot_resized = cv2.resize(slot_region, (64, 64))
                    
                    # Classify
                    result = st.session_state.clf.classify_crop(slot_resized)
                    
                    results.append({
                        'slot_id': slot['id'],
                        'label': slot['label'],
                        'x': x,
                        'y': y,
                        'w': w,
                        'h': h,
                        'status': 'OCCUPIED' if result['has_vehicle'] else 'VACANT',
                        'confidence': result['confidence']
                    })
                
                st.session_state.analysis_results = results
                st.success(f"✓ Analyzed {len(results)} slots")
        
        # Display results
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            if results:
                # Calculate statistics
                occupied = sum(1 for r in results if r['status'] == 'OCCUPIED')
                vacant = sum(1 for r in results if r['status'] == 'VACANT')
                total = len(results)
                occupancy_rate = (occupied / total * 100) if total > 0 else 0
                
                # Display statistics in columns
                st.markdown("---")
                st.subheader("📊 Analysis Results")
                
                stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                
                with stats_col1:
                    st.metric("Total Spaces", total, delta=None)
                
                with stats_col2:
                    st.metric("Occupied", occupied, delta=f"{occupied/total*100:.1f}%", delta_color="inverse")
                
                with stats_col3:
                    st.metric("Vacant", vacant, delta=f"{vacant/total*100:.1f}%", delta_color="normal")
                
                with stats_col4:
                    st.metric("Occupancy Rate", f"{occupancy_rate:.1f}%")
                
                # Visualization - Create annotated image
                viz_col1, viz_col2 = st.columns([2, 1])
                
                with viz_col1:
                    # Draw rectangles on image
                    annotated_image = image_rgb.copy()
                    for result in results:
                        x, y, w, h = result['x'], result['y'], result['w'], result['h']
                        color = (220, 20, 60) if result['status'] == 'OCCUPIED' else (34, 139, 34)  # Red or Green
                        cv2.rectangle(annotated_image, (x, y), (x+w, y+h), color, 2)
                        
                        # Add label
                        label_text = f"{result['label']}"
                        cv2.putText(annotated_image, label_text, (x+5, y+20), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
                    st.image(annotated_image, caption="Parking Lot Analysis (Red=Occupied, Green=Vacant)", 
                            use_column_width=True)
                
                with viz_col2:
                    try:
                        import plotly.graph_objects as go
                        # Pie chart
                        fig = go.Figure(data=[go.Pie(
                            labels=['Occupied', 'Vacant'],
                            values=[occupied, vacant],
                            marker=dict(colors=['#DC143C', '#228B22']),
                            hoverinfo='label+value+percent'
                        )])
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    except:
                        st.write("📊 Parking Lot Stats")
                        st.write(f"🔴 Occupied: {occupied}")
                        st.write(f"🟢 Vacant: {vacant}")
                
                # Detailed results table
                st.subheader("🔍 Detailed Slot Analysis")
                
                results_sorted = sorted(results, key=lambda x: x['label'])
                
                for i in range(0, len(results_sorted), 4):
                    row_results = results_sorted[i:i+4]
                    cols_display = st.columns(len(row_results))
                    
                    for idx, result in enumerate(row_results):
                        with cols_display[idx]:
                            status_emoji = '🔴' if result['status'] == 'OCCUPIED' else '🟢'
                            st.markdown(f"""
                            **{result['label']}** {status_emoji}
                            
                            {result['status']}
                            
                            Conf: {result['confidence']:.1%}
                            """)
        
        elif st.session_state.slots:
            st.info(f"✓ {len(st.session_state.slots)} slots defined. Click 'Analyze All Slots' to begin detection.")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        import traceback
        st.error(traceback.format_exc())

elif uploaded_file and not st.session_state.model_loaded:
    st.warning("⚠️ Please load the model first!")

# Info sections
with st.expander("ℹ️ How It Works"):
    st.markdown("""
    ### Multi-Slot Detection Pipeline
    
    1. **Image Upload**: Submit a parking lot image
    2. **Slot Definition**: Define parking spaces (auto-grid, manual, or upload config)
    3. **Per-Slot Analysis**: Our ResNet18 model analyzes each space
    4. **Classification**: Each space is classified as OCCUPIED or VACANT
    5. **Statistics**: Get occupancy count, rate, and visualization
    
    ### What You Get
    - ✅ Total number of parking spaces
    - ✅ Count of occupied spaces
    - ✅ Count of vacant spaces
    - ✅ Occupancy percentage
    - ✅ Visual overlay with colored rectangles
    - ✅ Confidence scores per space
    """)

with st.expander("🎯 Tips for Best Results"):
    st.markdown("""
    - **Aerial View**: Best results with overhead/drone photography
    - **Clear Spaces**: Ensure parking spaces are clearly defined
    - **Good Lighting**: Daytime with good visibility recommended
    - **Resolution**: Higher resolution = better detection
    - **Grid Size**: Match grid to actual parking lot layout
    - **Spacing**: Ensure spaces in grid don't overlap
    """)

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666;">
    <p>🅿️ Parking Lot Analyzer | ResNet18 + PyTorch + Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
