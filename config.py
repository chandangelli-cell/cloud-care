import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Base Configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cloudcare-dev-secret-key-change-in-prod-8877')
    
    # Database
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = db_url or f"sqlite:///{os.path.join(basedir, 'cloudcare.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
    }

    # Uploads & Cloud Storage
    STORAGE_PROVIDER = os.environ.get('STORAGE_PROVIDER', 'local')  # 'local', 'aws_s3', 'azure_blob'
    upload_folder_env = os.environ.get('UPLOAD_FOLDER', 'uploads')
    UPLOAD_FOLDER = upload_folder_env if os.path.isabs(upload_folder_env) else os.path.join(basedir, upload_folder_env)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

    # AWS S3 / S3-Compatible Settings (Cloudflare R2 / Supabase Storage / MinIO)
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    AWS_ENDPOINT_URL = os.environ.get('AWS_ENDPOINT_URL')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'cloudcare-medical-reports')

    # Azure Blob Settings
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    AZURE_CONTAINER_NAME = os.environ.get('AZURE_CONTAINER_NAME', 'cloudcare-reports')

    # Security & Session Settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    # Hospital Settings
    HOSPITAL_NAME = "CloudCare Smart Hospital"
    HOSPITAL_TIMEZONE = os.environ.get('HOSPITAL_TIMEZONE', 'UTC')
    DEFAULT_APPOINTMENT_DURATION_MINUTES = 30
    DEFAULT_CONSULTATION_FEE = 100.00


class DevelopmentConfig(Config):
    """Development Configuration."""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    """Testing Configuration."""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    STORAGE_PROVIDER = 'local'
    UPLOAD_FOLDER = os.path.join(basedir, 'test_uploads')


class ProductionConfig(Config):
    """Production Cloud Configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    # In production, require actual SECRET_KEY to be set in environment
    if not os.environ.get('SECRET_KEY'):
        SECRET_KEY = 'cloudcare-secure-prod-key-please-set-env'


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
