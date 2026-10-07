from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
)
from datetime import datetime


DATABASE_URL = "sqlite:///data/logiscan.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_name = Column(
        String(255),
        nullable=False,
        index=True
    )

    address = Column(
        Text,
        nullable=True
    )

    phone_numbers = Column(
        Text,
        nullable=True
    )

    emails = Column(
        Text,
        nullable=True
    )

    gst_number = Column(
        String(50),
        nullable=True,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    documents = relationship(
        "Document",
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    document_type = Column(
        String(100),
        nullable=True
    )

    invoice_number = Column(
        String(100),
        nullable=True,
        index=True
    )

    invoice_date = Column(
        String(50),
        nullable=True
    )

    bank_name = Column(
        String(255),
        nullable=True
    )

    account_number = Column(
        String(100),
        nullable=True
    )

    ifsc_code = Column(
        String(50),
        nullable=True
    )

    source_file = Column(
        String(500),
        nullable=True
    )

    raw_ocr_text = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    customer = relationship(
        "Customer",
        back_populates="documents"
    )


def create_tables():
    """
    Create database tables if they don't exist.
    """

    Base.metadata.create_all(
        bind=engine
    )