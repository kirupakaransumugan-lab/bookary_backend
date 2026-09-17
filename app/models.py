from datetime import date, datetime

from sqlalchemy import String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    author: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    available: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )


class Member(Base):
    __tablename__ = "members"

    id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Active"
    )

    joined: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )



class Borrow(Base):
    __tablename__ = "borrows"

    id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    member_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("members.id"),
        nullable=False
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False
    )

    borrowed: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    due: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    returned: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Borrowed"
    )



class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="member"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

