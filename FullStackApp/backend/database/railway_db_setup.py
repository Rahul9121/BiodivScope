"""
Railway Database Setup Script
This script initializes all database tables and imports data for Railway PostgreSQL
"""
import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, text, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

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
    
    # Fix postgres:// to postgresql:// if needed (Railway sometimes uses postgres://)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url

# Database setup
DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Define database models
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class IUCNData(Base):
    __tablename__ = 'iucn_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    species_name = Column(Text)
    genus = Column(Text)
    family = Column(Text)
    threat_status = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    locality = Column(Text)

def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(engine)
        logger.info("✅ All tables created successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        return False

def setup_invasive_species_table():
    """Create invasive species table"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS invasive_species (
            id SERIAL PRIMARY KEY,
            species_name TEXT,
            common_name TEXT,
            genus TEXT,
            family TEXT,
            threat_level TEXT,
            habitat_type TEXT,
            latitude FLOAT,
            longitude FLOAT,
            location_name TEXT,
            control_methods TEXT,
            impact_severity TEXT
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        conn.close()
        logger.info("✅ Invasive species table created successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating invasive species table: {e}")
        return False

def setup_risk_assessment_tables():
    """Create risk assessment tables"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Freshwater risk table
        freshwater_table = """
        CREATE TABLE IF NOT EXISTS freshwater_risk (
            id SERIAL PRIMARY KEY,
            x FLOAT,
            y FLOAT,
            risk_level TEXT,
            hci_score FLOAT,
            species_count INTEGER,
            threat_factors TEXT
        );
        """
        
        # Marine risk table
        marine_table = """
        CREATE TABLE IF NOT EXISTS marine_hci (
            id SERIAL PRIMARY KEY,
            x FLOAT,
            y FLOAT,
            hci_value FLOAT,
            risk_category TEXT,
            ecosystem_type TEXT
        );
        """
        
        # Terrestrial risk table
        terrestrial_table = """
        CREATE TABLE IF NOT EXISTS terrestrial_risk (
            id SERIAL PRIMARY KEY,
            x FLOAT,
            y FLOAT,
            risk_score FLOAT,
            land_use_type TEXT,
            biodiversity_index FLOAT
        );
        """
        
        for table_query in [freshwater_table, marine_table, terrestrial_table]:
            cur.execute(table_query)
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("✅ Risk assessment tables created successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating risk assessment tables: {e}")
        return False

def create_database_indexes():
    """Create indexes for better performance"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
            "CREATE INDEX IF NOT EXISTS idx_iucn_data_coords ON iucn_data(latitude, longitude);",
            "CREATE INDEX IF NOT EXISTS idx_iucn_data_species ON iucn_data(species_name);",
            "CREATE INDEX IF NOT EXISTS idx_invasive_species_coords ON invasive_species(latitude, longitude);",
            "CREATE INDEX IF NOT EXISTS idx_freshwater_risk_coords ON freshwater_risk(x, y);",
            "CREATE INDEX IF NOT EXISTS idx_marine_hci_coords ON marine_hci(x, y);",
            "CREATE INDEX IF NOT EXISTS idx_terrestrial_risk_coords ON terrestrial_risk(x, y);"
        ]
        
        for index_query in indexes:
            cur.execute(index_query)
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("✅ Database indexes created successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating indexes: {e}")
        return False

def main():
    """Main setup function"""
    logger.info("🚀 Starting Railway database setup...")
    
    # Step 1: Create basic tables
    if not create_tables():
        logger.error("Failed to create basic tables")
        return False
    
    # Step 2: Create invasive species table
    if not setup_invasive_species_table():
        logger.error("Failed to create invasive species table")
        return False
    
    # Step 3: Create risk assessment tables
    if not setup_risk_assessment_tables():
        logger.error("Failed to create risk assessment tables")
        return False
    
    # Step 4: Create indexes
    if not create_database_indexes():
        logger.error("Failed to create indexes")
        return False
    
    logger.info("🎉 Database setup completed successfully!")
    logger.info("📊 Database is ready for data import!")
    
    return True

if __name__ == "__main__":
    main()
