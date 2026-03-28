import datetime
from typing import Optional
from sqlalchemy import Date, DateTime, Numeric, Text, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

# Model as per SQLAlchemy 2.0's Declarative Models
# https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#whatsnew-20-orm-declarative-typing

class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    address: Mapped[Optional[str]] = mapped_column(Text)
    date_of_birth: Mapped[Optional[datetime.date]] = mapped_column(Date)
    account_balance: Mapped[Optional[str]] = mapped_column(Numeric(15, 2), default=0)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
