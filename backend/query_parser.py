"""Natural Language Query Parser"""
import re
from typing import Optional
from models import ExtractedFilters

class QueryParser:
    """Parse natural language queries to extract structured filters"""
    
    CITIES = {
        'mumbai': ['mumbai', 'bombay', 'navi mumbai', 'chembur'],
        'pune': ['pune', 'pimpri', 'chinchwad', 'shivajinagar', 'wakad', 'baner'],
        'bangalore': ['bangalore', 'bengaluru'],
        'delhi': ['delhi', 'new delhi', 'ncr']
    }
    
    BHK_PATTERNS = [
        (r'(\d+)\s*bhk', lambda m: f"{m.group(1)}BHK"),
        (r'(one|1)\s*bedroom', lambda m: "1BHK"),
        (r'(two|2)\s*bedroom', lambda m: "2BHK"),
        (r'(three|3)\s*bedroom', lambda m: "3BHK"),
        (r'(four|4)\s*bedroom', lambda m: "4BHK"),
    ]
    
    POSSESSION_KEYWORDS = {
        'ready to move': ['ready', 'immediate', 'ready to move', 'rtm'],
        'under construction': ['under construction', 'upcoming', 'new launch']
    }
    
    def parse(self, query: str) -> ExtractedFilters:
        query_lower = query.lower()
        
        return ExtractedFilters(
            city=self._extract_city(query_lower),
            bhk=self._extract_bhk(query_lower),
            budget_min=self._extract_budget_min(query_lower),
            budget_max=self._extract_budget_max(query_lower),
            possession_status=self._extract_possession_status(query_lower),
            locality=self._extract_locality(query_lower),
            project_name=self._extract_project_name(query_lower)
        )
    
    def _extract_city(self, query: str) -> Optional[str]:
        for city, variations in self.CITIES.items():
            for variation in variations:
                if variation in query:
                    return city.title()
        return None
    
    def _extract_bhk(self, query: str) -> Optional[str]:
        for pattern, formatter in self.BHK_PATTERNS:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return formatter(match)
        return None
    
    def _extract_budget_max(self, query: str) -> Optional[float]:
        cr_pattern = r'(?:under|below|upto|up to|within|max|maximum)\s*₹?\s*(\d+\.?\d*)\s*(?:cr|crore|crores)'
        match = re.search(cr_pattern, query, re.IGNORECASE)
        if match:
            return float(match.group(1)) * 10000000
        
        lakh_pattern = r'(?:under|below|upto|up to|within|max|maximum)\s*₹?\s*(\d+\.?\d*)\s*(?:l|lakh|lakhs)'
        match = re.search(lakh_pattern, query, re.IGNORECASE)
        if match:
            return float(match.group(1)) * 100000
        
        return None
    
    def _extract_budget_min(self, query: str) -> Optional[float]:
        cr_pattern = r'(?:above|over|from|starting from|minimum|min)\s*₹?\s*(\d+\.?\d*)\s*(?:cr|crore|crores)'
        match = re.search(cr_pattern, query, re.IGNORECASE)
        if match:
            return float(match.group(1)) * 10000000
        
        range_pattern = r'between\s*₹?\s*(\d+\.?\d*)\s*(?:-|to|and)\s*₹?\s*(\d+\.?\d*)\s*(?:cr|crore)'
        match = re.search(range_pattern, query, re.IGNORECASE)
        if match:
            return float(match.group(1)) * 10000000
        
        return None
    
    def _extract_possession_status(self, query: str) -> Optional[str]:
        for status, keywords in self.POSSESSION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query:
                    return status.title()
        return None
    
    def _extract_locality(self, query: str) -> Optional[str]:
        locality_pattern = r'(?:in|at|near)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        match = re.search(locality_pattern, query)
        if match:
            potential_locality = match.group(1)
            if potential_locality.lower() not in ['pune', 'mumbai', 'bangalore', 'delhi']:
                return potential_locality
        return None
    
    def _extract_project_name(self, query: str) -> Optional[str]:
        project_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:project|apartments|residency|heights|towers)'
        match = re.search(project_pattern, query)
        if match:
            return match.group(1)
        return None
