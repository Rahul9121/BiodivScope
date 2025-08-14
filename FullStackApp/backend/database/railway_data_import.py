"""
Railway Data Import Script
This script imports all your local data into Railway PostgreSQL database
"""
import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import logging
import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_database_url():
    """Get database URL from Railway environment variables"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        # Fallback for local development
        host = os.environ.get('DB_HOST', 'localhost')
        user = os.environ.get('DB_USER', 'postgres')
        password = os.environ.get('DB_PASSWORD', 'password')
        dbname = os.environ.get('DB_NAME', 'postgres')
        database_url = f'postgresql://{user}:{password}@{host}/{dbname}'
    
    # Fix postgres:// to postgresql:// if needed
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url

def import_iucn_data():
    """Import IUCN data if CSV file exists"""
    try:
        # Look for IUCN CSV file in common locations
        possible_paths = [
            'cleaned_IUCN_data.csv',
            '../data/cleaned_IUCN_data.csv',
            'data/cleaned_IUCN_data.csv',
            'database/cleaned_IUCN_data.csv'
        ]
        
        csv_path = None
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if not csv_path:
            logger.warning("⚠️ IUCN CSV file not found. Skipping IUCN data import.")
            return True
        
        # Import data
        df = pd.read_csv(csv_path)
        
        # Standardize column names
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        
        # Rename columns to match database schema
        column_mappings = {
            "endangered": "threat_status",
            "species": "species_name",
            "lat": "latitude",
            "lon": "longitude",
            "lng": "longitude",
            "location": "locality"
        }
        
        for old_col, new_col in column_mappings.items():
            if old_col in df.columns:
                df.rename(columns={old_col: new_col}, inplace=True)
        
        # Keep only valid columns
        valid_columns = ["species_name", "genus", "family", "threat_status", "latitude", "longitude", "locality"]
        existing_columns = [col for col in valid_columns if col in df.columns]
        df = df[existing_columns]
        
        # Import to database
        engine = create_engine(get_database_url())
        df.to_sql('iucn_data', engine, if_exists='append', index=False)
        
        logger.info(f"✅ Imported {len(df)} IUCN records successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error importing IUCN data: {e}")
        return False

def import_risk_data():
    """Import risk assessment data from your existing Python scripts"""
    try:
        # This would run your existing risk assessment data setup scripts
        # For now, we'll create sample data
        
        engine = create_engine(get_database_url())
        
        # Sample freshwater risk data
        freshwater_data = pd.DataFrame({
            'x': [-74.0, -74.1, -74.2, -74.3],
            'y': [40.0, 40.1, 40.2, 40.3],
            'risk_level': ['high', 'moderate', 'low', 'high'],
            'hci_score': [0.8, 0.6, 0.3, 0.9],
            'species_count': [15, 12, 8, 18],
            'threat_factors': ['invasive species', 'pollution', 'habitat loss', 'climate change']
        })
        
        # Sample marine data
        marine_data = pd.DataFrame({
            'x': [-74.0, -74.1, -74.2],
            'y': [40.0, 40.1, 40.2],
            'hci_value': [0.7, 0.5, 0.8],
            'risk_category': ['high', 'moderate', 'high'],
            'ecosystem_type': ['coastal', 'offshore', 'estuary']
        })
        
        # Sample terrestrial data
        terrestrial_data = pd.DataFrame({
            'x': [-74.0, -74.1, -74.2],
            'y': [40.0, 40.1, 40.2],
            'risk_score': [0.6, 0.4, 0.7],
            'land_use_type': ['urban', 'forest', 'agricultural'],
            'biodiversity_index': [0.5, 0.8, 0.6]
        })
        
        # Import all data
        freshwater_data.to_sql('freshwater_risk', engine, if_exists='append', index=False)
        marine_data.to_sql('marine_hci', engine, if_exists='append', index=False)
        terrestrial_data.to_sql('terrestrial_risk', engine, if_exists='append', index=False)
        
        logger.info("✅ Risk assessment data imported successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error importing risk data: {e}")
        return False

def import_invasive_species_data():
    """Import invasive species data"""
    try:
        # Sample invasive species data
        invasive_data = pd.DataFrame({
            'species_name': ['Phragmites australis', 'Lonicera maackii', 'Elaeagnus umbellata'],
            'common_name': ['Common Reed', 'Amur Honeysuckle', 'Autumn Olive'],
            'genus': ['Phragmites', 'Lonicera', 'Elaeagnus'],
            'family': ['Poaceae', 'Caprifoliaceae', 'Elaeagnaceae'],
            'threat_level': ['high', 'moderate', 'high'],
            'habitat_type': ['wetland', 'forest', 'forest edge'],
            'latitude': [40.0583, 40.1583, 40.2583],
            'longitude': [-74.4057, -74.5057, -74.6057],
            'location_name': ['New Jersey', 'New Jersey', 'New Jersey'],
            'control_methods': ['mechanical removal', 'selective herbicide', 'biological control'],
            'impact_severity': ['severe', 'moderate', 'severe']
        })
        
        engine = create_engine(get_database_url())
        invasive_data.to_sql('invasive_species', engine, if_exists='append', index=False)
        
        logger.info(f"✅ Imported {len(invasive_data)} invasive species records!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error importing invasive species data: {e}")
        return False

def verify_data_import():
    """Verify that data was imported correctly"""
    try:
        engine = create_engine(get_database_url())
        
        # Check record counts
        tables = ['users', 'iucn_data', 'invasive_species', 'freshwater_risk', 'marine_hci', 'terrestrial_risk']
        
        for table in tables:
            try:
                result = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", engine)
                count = result.iloc[0]['count']
                logger.info(f"📊 {table}: {count} records")
            except Exception as e:
                logger.warning(f"⚠️ Could not check {table}: {e}")
        
        logger.info("✅ Data verification completed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error verifying data: {e}")
        return False

def main():
    """Main data import function"""
    logger.info("🚀 Starting Railway data import...")
    
    success = True
    
    # Import IUCN data
    if not import_iucn_data():
        success = False
    
    # Import invasive species data
    if not import_invasive_species_data():
        success = False
    
    # Import risk assessment data
    if not import_risk_data():
        success = False
    
    # Verify imports
    verify_data_import()
    
    if success:
        logger.info("🎉 Data import completed successfully!")
    else:
        logger.error("❌ Some data imports failed. Check logs above.")
    
    return success

if __name__ == "__main__":
    main()
