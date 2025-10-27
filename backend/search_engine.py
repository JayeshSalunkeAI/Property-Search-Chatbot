"""Search Engine for Property Retrieval"""
import pandas as pd
from typing import List, Dict
from models import PropertyCard, ExtractedFilters

class SearchEngine:
    """Search and retrieve properties from CSV data"""
    
    def __init__(self, data_path: str = "data/"):
        self.data_path = data_path
        self.df = self._load_and_merge_data()
    
    def _load_and_merge_data(self) -> pd.DataFrame:
        """Load all CSV files and merge into single DataFrame"""
        # Load all tables
        projects = pd.read_csv(f"{self.data_path}project.csv")
        addresses = pd.read_csv(f"{self.data_path}ProjectAddress.csv")
        configs = pd.read_csv(f"{self.data_path}ProjectConfiguration.csv")
        variants = pd.read_csv(f"{self.data_path}ProjectConfigurationVariant.csv")
        
        # Merge tables
        df = projects.merge(addresses, left_on='id', right_on='projectId', how='left', suffixes=('', '_addr'))
        df = df.merge(configs, left_on='id', right_on='projectId', how='left', suffixes=('', '_config'))
        df = df.merge(variants, left_on='id_config', right_on='configurationId', how='left', suffixes=('', '_variant'))
        
        return df
    
    def search(self, filters: ExtractedFilters) -> List[PropertyCard]:
        """
        Search properties based on extracted filters
        
        Args:
            filters: ExtractedFilters object with search parameters
            
        Returns:
            List of PropertyCard objects matching filters
        """
        df = self.df.copy()
        
        # Apply city filter
        if filters.city:
            # Simple filter - you can enhance with city ID mapping
            df = df[df['fullAddress'].str.contains(filters.city, case=False, na=False)]
        
        # Apply BHK filter
        if filters.bhk:
            df = df[df['type'] == filters.bhk]
        
        # Apply budget filters
        if filters.budget_max:
            df = df[df['price'] <= filters.budget_max]
        
        if filters.budget_min:
            df = df[df['price'] >= filters.budget_min]
        
        # Apply possession status filter
        if filters.possession_status:
            status_map = {
                'Ready To Move': 'READY_TO_MOVE',
                'Under Construction': 'UNDER_CONSTRUCTION'
            }
            mapped_status = status_map.get(filters.possession_status)
            if mapped_status:
                df = df[df['status'] == mapped_status]
        
        # Apply locality filter
        if filters.locality:
            df = df[df['fullAddress'].str.contains(filters.locality, case=False, na=False)]
        
        # Apply project name filter
        if filters.project_name:
            df = df[df['projectName'].str.contains(filters.project_name, case=False, na=False)]
        
        # Convert to PropertyCard objects
        properties = []
        for _, row in df.head(10).iterrows():  # Limit to 10 results
            properties.append(self._row_to_property_card(row))
        
        return properties
    
    def _row_to_property_card(self, row) -> PropertyCard:
        """Convert DataFrame row to PropertyCard"""
        # Format price
        price_raw = row.get('price', 0)
        if pd.notna(price_raw):
            if price_raw >= 10000000:
                price_formatted = f"₹{price_raw/10000000:.2f} Cr"
            else:
                price_formatted = f"₹{price_raw/100000:.2f} L"
        else:
            price_formatted = "Price on request"
        
        # Extract amenities
        amenities = []
        if row.get('lift'):
            amenities.append('Lift')
        if row.get('parkingType'):
            amenities.append('Parking')
        if row.get('balcony', 0) > 0:
            amenities.append(f"{int(row['balcony'])} Balconies")
        
        # Status mapping
        status_display = row.get('status', '').replace('_', ' ').title()
        
        return PropertyCard(
            project_id=row.get('id', ''),
            title=row.get('projectName', 'Unnamed Project'),
            city=self._extract_city_from_address(row.get('fullAddress', '')),
            locality=row.get('landmark', 'Location details available'),
            bhk=row.get('type', 'N/A'),
            price=price_formatted,
            price_raw=price_raw if pd.notna(price_raw) else 0,
            project_name=row.get('projectName', 'Unnamed Project'),
            possession_status=status_display,
            amenities=amenities[:3],  # Top 3 amenities
            carpet_area=row.get('carpetArea'),
            bathrooms=row.get('bathrooms'),
            balconies=row.get('balcony'),
            slug=row.get('slug', ''),
            url=f"/project/{row.get('slug', '')}"
        )
    
    def _extract_city_from_address(self, address: str) -> str:
        """Extract city name from full address"""
        if 'mumbai' in address.lower():
            return 'Mumbai'
        elif 'pune' in address.lower():
            return 'Pune'
        elif 'bangalore' in address.lower():
            return 'Bangalore'
        else:
            return 'India'
