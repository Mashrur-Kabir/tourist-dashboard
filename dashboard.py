import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Page Setup ---
st.set_page_config(page_title="Tourist Informatics", layout="wide")
st.title("🌍 Tourist Informatics")

# --- Sidebar: File Upload ---
st.sidebar.header("📂 Upload Your Data File")
uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

# Required columns for validation
required_cols = ["Name", "Country", "Destination", "Duration", "Rating"]

# --- Function to Load and Validate File ---
def load_data(file):
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            return None, "Unsupported file format"
        
        # Check for required columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return None, f"Missing columns: {', '.join(missing_cols)}"
        
        return df, None
    except Exception as e:
        return None, str(e)

# --- Main Interface ---
if uploaded_file is not None:
    df, error = load_data(uploaded_file)

    if error:
        st.error(f"❌ Error: {error}")
    else:
        st.success("✅ File loaded successfully!")

        # --- Inputs ---
        st.sidebar.subheader("🔘 Filter Tourists")
        # Radio button for country selection
        countries = sorted(df["Country"].dropna().unique())
        country = st.sidebar.radio("Select Country", ["All"] + countries)

        # Dropdown for destination selection
        destinations = sorted(df["Destination"].dropna().unique())
        destination = st.sidebar.selectbox("Select Destination", ["All"] + destinations)

        # Apply filters
        filtered_df = df.copy()
        if country != "All":
            filtered_df = filtered_df[filtered_df["Country"] == country]
        if destination != "All":
            filtered_df = filtered_df[filtered_df["Destination"] == destination]

        # --- Display Data Table ---
        st.subheader("📋 Filtered Tourist Data")
        st.dataframe(filtered_df, use_container_width=True)

        # --- Summary Stats ---
        st.subheader("📈 Summary")
        if not filtered_df.empty:
            avg_duration = filtered_df["Duration"].mean()
            avg_rating = filtered_df["Rating"].mean()
            st.markdown(f"- **Average Duration:** `{avg_duration:.2f}` days")
            st.markdown(f"- **Average Rating:** `{avg_rating:.2f}` out of 5")
        else:
            st.warning("No data found for the selected filters.")

        # --- Visualizations ---
        if not filtered_df.empty:
            st.subheader("📊 Visual Insights")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🌍 Destination Distribution (Pie Chart)")
                pie_data = filtered_df["Destination"].value_counts()
                fig1, ax1 = plt.subplots()
                ax1.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
                ax1.axis("equal")
                st.pyplot(fig1)

            with col2:
                st.markdown("### ⭐ Tourist Ratings (Bar Chart)")
                bar_data = filtered_df["Rating"].value_counts().sort_index()
                fig2, ax2 = plt.subplots()
                bar_data.plot(kind="bar", ax=ax2)
                ax2.set_xlabel("Rating")
                ax2.set_ylabel("Number of Tourists")
                st.pyplot(fig2)
        else:
            st.info("📭 No data to visualize.")

        # --- Download Filtered Data ---
        st.subheader("⬇️ Download Filtered Data")
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download as CSV", data=csv, file_name="filtered_tourists.csv", mime="text/csv")

else:
    st.info("👈 Please upload a file from the sidebar to begin.")
