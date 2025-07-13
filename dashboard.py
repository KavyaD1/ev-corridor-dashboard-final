import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import PolyLine
import pandas as pd
from geopy.distance import geodesic

# Corridor data
corridor_data = {
    "Ambala – Jalandhar": [
        {
            "id": "X1",
            "place": "Dera Bassi",
            "coordinates": [30.5445, 76.8215],
            "substation": [30.5488, 76.8260],
            "renewables": [30.5502, 76.8185],
            "highway": "NH-152",
            "contact": "goldenhutresorts.com | 074004 56000"
        },
        {
            "id": "X2",
            "place": "Kurukshetra",
            "coordinates": [29.9459, 76.8994],
            "substation": [29.9679, 76.8783],
            "renewables": [29.9500, 76.8500],
            "highway": "NH-44",
            "contact": "097285 16312"
        },
        {
            "id": "X3",
            "place": "Uchana",
            "coordinates": [29.745, 76.9726],
            "substation": [29.7300, 76.9800],
            "renewables": [29.7350, 76.9600],
            "highway": "GT Road",
            "contact": "+91 172 2702955"
        }
    ],
    "Chennai – Bengaluru": [
        {
            "id": "D1",
            "place": "Vellore",
            "coordinates": [12.977316, 79.23933],
            "substation": [12.9360, 79.1450],
            "renewables": [13.0000, 79.0000],
            "highway": "NH-48",
            "distanceFromHighway": "15-20 km",
            "siteSize": "Unknown",
            "amenities": "OYO Hasini Inn (~1.76 km)",
            "contact": "Vellore_sugars@yahoo.co.in"
        },
        {
            "id": "D2",
            "place": "Palamaner",
            "coordinates": [13.2049685, 78.7302713],
            "substation": [13.2000, 78.7200],
            "renewables": [13.2500, 78.8500],
            "highway": "NH-45",
            "distanceFromHighway": "Direct access",
            "siteSize": "700 m²",
            "amenities": "RR Paradise Restaurant",
            "contact": "090667 39008"
        },
        {
            "id": "D3",
            "place": "Nagavara",
            "coordinates": [13.0939404, 77.5923877],
            "substation": [13.0700, 77.6200],
            "renewables": [12.7400, 77.8300],
            "highway": "NH-44",
            "distanceFromHighway": "~5 km",
            "siteSize": "875 m²",
            "amenities": "Heavy vehicles paid parking (~120 m)",
            "contact": "https://english.bmrc.co.in/"
        }
    ],
    "Bhiwadi – Jaipur": [
        {
            "id": "B1",
            "place": "Manesar",
            "coordinates": [28.3573, 76.9366],
            "substation": [28.3605, 76.9466],
            "renewables": [28.3582, 76.9350],
            "highway": "NH 48",
            "siteSize": "1800 sqm (~0.45 acres)",
            "distanceFromHighway": "200 m",
            "amenities": "Suitable for EV Truck Station",
            "contact": "+91-98184-23456"
        },
        {
            "id": "B2",
            "place": "Rewari Bypass",
            "coordinates": [28.197, 76.619],
            "substation": [28.207, 76.619],
            "renewables": [28.197, 76.619],
            "highway": "NH 48",
            "siteSize": "1600 sqm (~0.40 acres)",
            "distanceFromHighway": "100 m",
            "amenities": "Suitable for EV Truck Station",
            "contact": "+91-99922-34567"
        },
        {
            "id": "B3",
            "place": "Kotputli",
            "coordinates": [27.7, 76.2],
            "substation": [27.685, 76.2],
            "renewables": [27.696, 76.198],
            "highway": "NH 48",
            "siteSize": "2500 sqm (~0.62 acres)",
            "distanceFromHighway": "150 m",
            "amenities": "Suitable for EV Truck Station",
            "contact": "+91-97811-45678"
        },
        {
            "id": "B4",
            "place": "Jaipur (Ring Road)",
            "coordinates": [26.9124, 75.7873],
            "substation": [26.894, 75.7873],
            "renewables": [26.9096, 75.7840],
            "highway": "NH 48",
            "siteSize": "3500 sqm (~0.86 acres)",
            "distanceFromHighway": "200 m",
            "amenities": "Suitable for EV Truck Station",
            "contact": "+91-98877-56789"
        }
    ],
    "Kolkata-Haldia":[
 {
  "id": "G1",
  "place": "Kasba",
  "coordinates": [22.57350556, 88.40230026],
  "corridor": "Kolkata–Haldia",
  "highway": "EM Bypass, NH 16 (~3 km)",
  "distanceFromHighway": "3 km",
  "siteSize": "4,694.57 m²",
  "amenities": "Bharat Petroleum pumps on EM Bypass (~1–2 km away)",
  "substation": [22.5580, 88.3900],  # Approximate coords for CESC Kasba Substation
  "renewables": [22.5600, 88.4100],  # Approximate solar potential location
  "contact": "https://www.seleqtionshotels.com/taj-raajkutir-kolkata/ | +91 33 6820 0800"
}

],
"Delhi-Chandhigarh":[
  {
    "id": "H1",
    "place": "Karnal",
    "coordinates": [29.6850, 76.9900],
    "corridor": "Delhi – Chandigarh",
    "highway": "NH 44",
    "distanceFromHighway": "2.5 km",
    "siteSize": "9000 m²",
    "amenities": "Agro park, dhaba (~700 m), warehouse (~1 km)",
    "substation": [29.6900, 76.9750],  
    "renewables": [29.6700, 76.9800], 
    "contact": "agro.karnal@hry.nic.in | +91-184-2257802"
  },
  {
    "id": "H2",
    "place": "Ambala",
    "coordinates": [30.3780, 76.7760],
    "corridor": "Delhi – Chandigarh",
    "highway": "NH 44",
    "distanceFromHighway": "3.8 km",
    "siteSize": "8500 m²",
    "amenities": "Industrial sheds (~1 km), rest stop (~600 m), dhaba (~400 m)",
    "substation": [30.3790, 76.7700],  
    "renewables": [30.3750, 76.7650],  
    "contact": "ambala.grid@pspcl.in | +91-171-2630033"
  },
  {
    "id": "H3",
    "place": "Sonipat",
    "coordinates": [28.9951, 77.0110],
    "corridor": "Delhi – Chandigarh",
    "highway": "NH 44",
    "distanceFromHighway": "2.0 km",
    "siteSize": "9500 m²",
    "amenities": "Truck halt (~500 m), freight terminal (~1 km)",
    "substation": [29.0000, 77.0000],  
    "renewables": [28.9900, 77.0050],  
    "contact": "sonipat.zone@hsiidc.org | +91-130-2242003"
  }
],
"Dhanbad-Kolkata":[
  {
    "id": "I1",
    "place": "Panagarh",
    "truckStopName": "Panagarh Truck Stop",
    "coordinates": [23.47, 87.43],
    "corridor": "Dhanbad – Kolkata Corridor",
    "highway": "NH-19",
    "distanceFromHighway": "unknown",
    "siteSize": "unknown",
    "amenities": "Near 3 MW solar, NH-19, industrial zone",
    "substation": [23.465, 87.425],  
    "renewables": [23.468, 87.420],  
    "contact": "cmc.durgapur@wbsedcl.in | 0343-2557771"
  },
  {
    "id": "I2",
    "place": "Durgapur Bypass",
    "truckStopName": "Durgapur Bypass Bay",
    "coordinates": [23.55, 87.29],
    "corridor": "Dhanbad – Kolkata Corridor",
    "highway": "NH-19",
    "distanceFromHighway": "unknown",
    "siteSize": "unknown",
    "amenities": "Mid-corridor, near thermal, grid, highway-side lay-by",
    "substation": [23.545, 87.295],  
    "renewables": [23.550, 87.285],  
    "contact": "ce.durgapur@wbsedcl.in | 0343-2545842"
  },
  {
    "id": "I3",
    "place": "Raniganj",
    "truckStopName": "Raniganj Truck Stand",
    "coordinates": [23.6250, 87.1380],
    "corridor": "Dhanbad – Kolkata Corridor",
    "highway": "NH-19",
    "distanceFromHighway": "unknown",
    "siteSize": "unknown",
    "amenities": "Truck stand close to DVC grid, logistics zone, NH-19",
    "substation": [23.622, 87.135],  
    "renewables": [23.620, 87.130],  
    "contact": "sdo.raniganj@wbsedcl.in | 0341-2446789"
  },
  {
    "id": "I4",
    "place": "Dankuni",
    "truckStopName": "Dankuni Truck Terminal",
    "coordinates": [22.67, 88.30],
    "corridor": "Dhanbad – Kolkata Corridor",
    "highway": "NH-19",
    "distanceFromHighway": "unknown",
    "siteSize": "unknown",
    "amenities": "Large urban logistics terminal, grid access",
    "substation": [22.668, 88.298],  
    "renewables": [22.665, 88.295],  
    "contact": "ce.hooghly@wbsetcl.in | 033-26382345"
  },
  {
    "id": "I5",
    "place": "Jharia",
    "truckStopName": "Jharia Truck Stand",
    "coordinates": [23.7957, 86.4304],
    "corridor": "Dhanbad – Kolkata Corridor",
    "highway": "NH-19",
    "distanceFromHighway": "unknown",
    "siteSize": "unknown",
    "amenities": "Major truck hub near thermal plant and DVC grid",
    "substation": [23.793, 86.435],  
    "renewables": [23.790, 86.430],  
    "contact": "dvc.jharia@dvc.gov.in | 06542-220145"
  }
],
"Paradeep-Barbil":[
  {
    "id": "L1",
    "place": "Site L1",
    "coordinates": [21.246574, 86.1355386],
    "corridor": "Paradeep – Barbil",
    "highway": "NH 53",
    "distanceFromHighway": "0.65 km",
    "siteSize": "Unknown",
    "amenities": "~1.2 km",
    "substation": "DRDA sub-station",
    "renewables": "Unknown",
    "contact": "Tel: 1242571700"
  },
  {
    "id": "L2",
    "place": "Site L2",
    "coordinates": [20.7670378, 86.3466015],
    "corridor": "Paradeep – Barbil",
    "highway": "NH 53",
    "distanceFromHighway": "1.92 km",
    "siteSize": "Unknown",
    "amenities": "~0.5 km",
    "substation": "Jaipur town grid substation (~16 km)",
    "renewables": "Unknown",
    "contact": "Tel: 7942698742"
  },
  {
    "id": "L3",
    "place": "Site L3",
    "coordinates": [20.8846845, 86.361322],
    "corridor": "Paradeep – Barbil",
    "highway": "NH 53, NH 20",
    "distanceFromHighway": "1.48 km",
    "siteSize": "Unknown",
    "amenities": "~1.5 km",
    "substation": "Jaipur town grid substation (OPTCL) (~5.66 km)",
    "renewables": "Unknown",
    "contact": "Tel: 1242571700"
  },
  {
    "id": "L4",
    "place": "Site L4",
    "coordinates": [21.246574, 86.1355386],
    "corridor": "Paradeep – Barbil",
    "highway": "NH 20",
    "distanceFromHighway": "1.32 km",
    "siteSize": "Unknown",
    "amenities": "2.1 km",
    "substation": "Duburi electric sub-station (~30 km)",
    "renewables": "Unknown",
    "contact": "Tel: +91 11 4103 4600, +91 11 4103 4601 (Email: info@powerline.net.in)"
  },
  {
    "id": "L5",
    "place": "Site L5",
    "coordinates": [21.3036207, 85.3944443],
    "corridor": "Paradeep – Barbil",
    "highway": "NH 520",
    "distanceFromHighway": "1.54 km",
    "siteSize": "Unknown",
    "amenities": "1.8 km",
    "substation": "New Duburi substation 400kV (~50 km)",
    "renewables": "Unknown",
    "contact": "Tel: 033-24235011 (Email: powergrid.pr@powergrid.in)"
  }
],
"Vijayawada – Hyderabad": [
        {
            "id": "n1",
            "place": "Kodad (Bypass)",
            "coordinates": [16.998, 79.976],
            "substation": [16.990, 79.960],  # approx from ~1.8km
            "renewables": [16.983, 79.970],  # approx from ~2.3km
            "highway": "NH 65",
            "distanceFromHighway": "2.5 km",
            "siteSize": "2200 m²",
            "amenities": "Sai Durga Family Dhaba (~1.2 km)",
            "owner": "Telangana Southern Power Distribution Company Ltd (TSSPDCL), Regional Division",
            "contact": "info@tssouthernpower.com | 1912"
        },
        {
            "id": "n2",
            "place": "Vijayawada",
            "coordinates": [16.5555, 80.6575],
            "substation": [16.5213, 80.635],  # approx from ~4.2km
            "renewables": [16.5655, 80.6455],  # approx from ~2.0km
            "highway": "NH 65",
            "distanceFromHighway": "2.0 km",
            "siteSize": "2000 m²",
            "amenities": "Highway Tiffins (~1.8 km)",
            "owner": "APSPDCL Vijayawada Division Office",
            "contact": "cmd@apspdcl.in | 0866-2573201"
        },
        {
            "id": "n3",
            "place": "Suryapet (Outskirts)",
            "coordinates": [17.140, 79.620],
            "substation": [17.135, 79.615],  # approx from ~1.0km
            "renewables": [17.130, 79.605],  # approx from ~2.5km
            "highway": "NH 65",
            "distanceFromHighway": "0.8 km",
            "siteSize": "2500 m²",
            "amenities": "Multiple dhabas and petrol pumps within 1 km",
            "owner": "TSSPDCL Suryapet Division",
            "contact": "ceop@tssouthernpower.com | 040-2313-2288"
        }
    ],
    
   
}



# Sidebar
st.sidebar.title("🗺️ Legend")
st.sidebar.markdown("""
- 🔵 **Station**  
- 🔴 **Substation**  
- 🟠 **Renewable Site**  
- 📏 **Distance Lines**
""")

# Title
st.title("🚚 EV Corridor Dashboard")

# Select Corridor and Station
selected_corridor = st.selectbox("Select EV Corridor", list(corridor_data.keys()))
site_list = corridor_data[selected_corridor]
site_names = [site["place"] for site in site_list]
selected_site = st.selectbox("Select Station", site_names)

# Get Site Data
site = next(item for item in site_list if item["place"] == selected_site)
station_coords = site.get("coordinates")
substation_coords = site.get("substation")
renewable_coords = site.get("renewables")

# Show map only if all coordinates are available
if station_coords and substation_coords and renewable_coords:
    # Calculate distances
    distance_to_substation = round(geodesic(station_coords, substation_coords).km, 2)
    distance_to_renewable = round(geodesic(station_coords, renewable_coords).km, 2)

    # Create map
    m = folium.Map(location=station_coords, zoom_start=13)
    folium.Marker(station_coords, tooltip="Station", popup=selected_site, icon=folium.Icon(color='blue')).add_to(m)
    folium.Marker(substation_coords, tooltip="Substation", popup=f"Substation ({distance_to_substation} km)", icon=folium.Icon(color='red')).add_to(m)
    folium.Marker(renewable_coords, tooltip="Renewables", popup=f"Renewable Site ({distance_to_renewable} km)", icon=folium.Icon(color='orange')).add_to(m)
    PolyLine([station_coords, substation_coords], color='black', weight=2.5, tooltip=f"Distance: {distance_to_substation} km").add_to(m)
    PolyLine([station_coords, renewable_coords], color='green', weight=2.5, tooltip=f"Distance: {distance_to_renewable} km").add_to(m)
    st_folium(m, width=700, height=500)

    # Download button
    df = pd.DataFrame([{
        "Corridor": selected_corridor,
        "Station": selected_site,
        "Station_Lat": station_coords[0],
        "Station_Lon": station_coords[1],
        "Substation_Lat": substation_coords[0],
        "Substation_Lon": substation_coords[1],
        "Renewables_Lat": renewable_coords[0],
        "Renewables_Lon": renewable_coords[1],
        "Distance to Substation (km)": distance_to_substation,
        "Distance to Renewables (km)": distance_to_renewable,
        "Highway": site.get("highway", "-"),
        "Distance from Highway": site.get("distanceFromHighway", "-"),
        "Site Size": site.get("siteSize", "-"),
        "Amenities": site.get("amenities", "-"),
        "Contact": site.get("contact", "-")
    }])

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Site Data as CSV",
        data=csv,
        file_name=f"{selected_corridor.replace(' ', '_')}_{selected_site}.csv",
        mime='text/csv'
    )
else:
    st.warning("🚫 Missing coordinate data for selected station. Map and download disabled.")
