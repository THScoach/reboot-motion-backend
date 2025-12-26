"""
Get PostgreSQL Database Schema
Shows all tables, columns, and their data types
"""
import os
from sqlalchemy import create_engine, inspect, text
import json

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL environment variable not set")
    print("\nTo get your database schema, you need to:")
    print("1. Go to Railway Dashboard → Postgres service")
    print("2. Go to 'Variables' tab")
    print("3. Copy the DATABASE_URL value")
    print("4. Run: export DATABASE_URL='your-connection-string-here'")
    print("5. Then run this script again")
    exit(1)

# Create engine
engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

print("=" * 80)
print("POSTGRESQL DATABASE SCHEMA")
print("=" * 80)
print()

# Get all table names
tables = inspector.get_table_names()
print(f"📊 Found {len(tables)} tables\n")

schema_info = {}

for table_name in sorted(tables):
    print(f"📋 Table: {table_name}")
    print("-" * 80)
    
    columns = inspector.get_columns(table_name)
    pk_constraint = inspector.get_pk_constraint(table_name)
    foreign_keys = inspector.get_foreign_keys(table_name)
    indexes = inspector.get_indexes(table_name)
    unique_constraints = inspector.get_unique_constraints(table_name)
    
    table_info = {
        'columns': [],
        'primary_keys': pk_constraint.get('constrained_columns', []),
        'foreign_keys': [],
        'indexes': [],
        'unique_constraints': []
    }
    
    # Columns
    for col in columns:
        col_info = {
            'name': col['name'],
            'type': str(col['type']),
            'nullable': col['nullable'],
            'default': str(col['default']) if col['default'] else None
        }
        table_info['columns'].append(col_info)
        
        nullable = "NULL" if col['nullable'] else "NOT NULL"
        default = f" DEFAULT {col['default']}" if col['default'] else ""
        pk = " 🔑 PRIMARY KEY" if col['name'] in table_info['primary_keys'] else ""
        
        print(f"  • {col['name']:<30} {str(col['type']):<20} {nullable:<10}{default}{pk}")
    
    # Foreign Keys
    if foreign_keys:
        print("\n  🔗 Foreign Keys:")
        for fk in foreign_keys:
            table_info['foreign_keys'].append({
                'columns': fk['constrained_columns'],
                'referred_table': fk['referred_table'],
                'referred_columns': fk['referred_columns']
            })
            cols = ', '.join(fk['constrained_columns'])
            ref_cols = ', '.join(fk['referred_columns'])
            print(f"    {cols} → {fk['referred_table']}({ref_cols})")
    
    # Unique Constraints
    if unique_constraints:
        print("\n  🎯 Unique Constraints:")
        for uc in unique_constraints:
            table_info['unique_constraints'].append({
                'name': uc['name'],
                'columns': uc['column_names']
            })
            cols = ', '.join(uc['column_names'])
            print(f"    {uc['name']}: ({cols})")
    
    # Indexes
    if indexes:
        print("\n  📇 Indexes:")
        for idx in indexes:
            table_info['indexes'].append({
                'name': idx['name'],
                'columns': idx['column_names'],
                'unique': idx['unique']
            })
            cols = ', '.join(idx['column_names'])
            unique = "UNIQUE" if idx['unique'] else ""
            print(f"    {idx['name']}: ({cols}) {unique}")
    
    schema_info[table_name] = table_info
    print()

print("=" * 80)
print("DATABASE CONNECTION INFO")
print("=" * 80)
print()
print(f"📍 Connection String Location:")
print(f"   Environment Variable: DATABASE_URL")
print()
print(f"🔗 Current Connection String:")
# Mask password in URL for security
import re
masked_url = re.sub(r'://([^:]+):([^@]+)@', r'://\1:****@', DATABASE_URL)
print(f"   {masked_url}")
print()

# Get database stats
with engine.connect() as conn:
    # Count records in each table
    print("=" * 80)
    print("RECORD COUNTS")
    print("=" * 80)
    print()
    
    for table_name in sorted(tables):
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.scalar()
        print(f"  {table_name:<30} {count:>10} records")
    print()

# Save schema to JSON file
with open('database_schema.json', 'w') as f:
    json.dump(schema_info, f, indent=2)
print("✅ Schema saved to: database_schema.json")
print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"✅ Database connection: SUCCESS")
print(f"✅ Tables found: {len(tables)}")
print(f"✅ Schema exported: database_schema.json")
print()
