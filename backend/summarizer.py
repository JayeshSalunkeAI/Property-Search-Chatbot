"""Summary Generation Logic"""
from typing import List
from models import PropertyCard, ExtractedFilters
import statistics

class Summarizer:
    """Generate intelligent summaries from search results"""
    
    def generate_summary(self, properties: List[PropertyCard], filters: ExtractedFilters) -> str:
        """
        Generate summary based on search results
        
        Args:
            properties: List of PropertyCard objects
            filters: Applied filters
            
        Returns:
            Human-readable summary string
        """
        if not properties:
            return self._generate_no_results_summary(filters)
        
        # Extract statistics
        total = len(properties)
        cities = list(set([p.city for p in properties]))
        localities = list(set([p.locality for p in properties]))[:3]
        bhk_types = list(set([p.bhk for p in properties]))
        prices = [p.price_raw for p in properties if p.price_raw > 0]
        avg_price = statistics.mean(prices) if prices else 0
        
        # Count statuses
        ready_count = sum(1 for p in properties if 'ready' in p.possession_status.lower())
        under_const_count = sum(1 for p in properties if 'construction' in p.possession_status.lower())
        
        # Build summary
        summary_parts = []
        
        # Opening statement
        if filters.budget_max:
            budget_str = f"₹{filters.budget_max/10000000:.1f} Cr" if filters.budget_max >= 10000000 else f"₹{filters.budget_max/100000:.0f} L"
            summary_parts.append(f"Found {total} properties under {budget_str}")
        else:
            summary_parts.append(f"Found {total} properties")
        
        # BHK info
        if filters.bhk:
            summary_parts.append(f"matching your {filters.bhk} requirement")
        
        # Location info
        if cities and len(cities) == 1:
            summary_parts.append(f"in {cities[0]}")
            if localities:
                locality_str = ", ".join(localities)
                summary_parts.append(f"primarily in {locality_str}")
        
        summary_line1 = " ".join(summary_parts) + "."
        
        # Second line - pricing and status
        summary_line2 = ""
        if avg_price > 0:
            avg_str = f"₹{avg_price/10000000:.2f} Cr" if avg_price >= 10000000 else f"₹{avg_price/100000:.0f} L"
            summary_line2 = f"Average price is around {avg_str}. "
        
        if ready_count > 0:
            summary_line2 += f"{ready_count} properties are ready to move. "
        if under_const_count > 0:
            summary_line2 += f"{under_const_count} are under construction. "
        
        # Third line - amenities
        all_amenities = []
        for p in properties:
            all_amenities.extend(p.amenities)
        common_amenities = list(set(all_amenities))[:3]
        
        summary_line3 = ""
        if common_amenities:
            amenity_str = ", ".join(common_amenities)
            summary_line3 = f"Common amenities include {amenity_str}."
        
        return f"{summary_line1} {summary_line2} {summary_line3}".strip()
    
    def _generate_no_results_summary(self, filters: ExtractedFilters) -> str:
        """Generate fallback summary when no results found"""
        parts = ["No properties found"]
        
        if filters.bhk:
            parts.append(f"for {filters.bhk}")
        
        if filters.city:
            parts.append(f"in {filters.city}")
        
        if filters.budget_max:
            budget_str = f"₹{filters.budget_max/10000000:.1f} Cr" if filters.budget_max >= 10000000 else f"₹{filters.budget_max/100000:.0f} L"
            parts.append(f"under {budget_str}")
        
        suggestion = " ".join(parts) + ". Try expanding your budget or exploring nearby localities."
        
        return suggestion
