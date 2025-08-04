"""Add password_hash to users table

Revision ID: 002_add_password_hash
Revises: 001_initial_tables
Create Date: 2025-08-04 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '002_add_password_hash'
down_revision = '001_initial_tables'
branch_labels = None
depends_on = None

def upgrade():
    # Add password_hash column to users table
    op.add_column('users', sa.Column('password_hash', sa.String(255), nullable=True))
    
    # Add default password hash for existing users (ONLY FOR DEVELOPMENT!)
    # In produzione, si dovrebbe richiedere agli utenti di impostare nuove password
    op.execute("UPDATE users SET password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewgVIq2EuLKGEWWq' WHERE password_hash IS NULL")
    # La password di default è: "password123"
    
    # Make password_hash required after setting default values
    op.alter_column('users', 'password_hash', nullable=False)

def downgrade():
    # Remove password_hash column
    op.drop_column('users', 'password_hash')
