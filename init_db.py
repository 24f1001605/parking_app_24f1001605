#!/usr/bin/env python3

import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from controllers.extensions import db
from models.models import User


def init_database():
    """Initialize database with tables and admin user"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully")
        
        # Create admin user if it doesn't exist
        admin_username = "admin"
        admin_password = "admin123"
        
        existing_admin = User.query.filter_by(username=admin_username).first()
        if not existing_admin:
            admin = User(username=admin_username, role="admin")
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created: username={admin_username}, password={admin_password}")
        else:
            print("Admin user already exists")
        
        print("\nDatabase initialization complete!")
        print("You can now run: python app.py")


if __name__ == "__main__":
    init_database() 