# core/utils/search.py
from sqlalchemy import select, or_
from sqlalchemy.orm import load_only
from sqlalchemy.sql.expression import func

from core.database import Database
from core.models import *

async def search(
    table: str,
    query: str,
    user_id: int
):
    db = Database()
    async with db.sessionmaker() as session:
        match table:
            case "people":
                return await search_people(query, user_id)
            case "properties":
                return await search_properties(query, user_id)
            case "transactions":
                return await search_transactions(query, user_id)

async def search_people(query: str, user_id: int):
    db = Database()
    async with db.sessionmaker() as session:
        if any(char.isdigit() for char in query):
            if sum(char.isdigit() for char in query) > 6:
                # Query only the phone column
                stmt = select(PersonOrm).where(
                    PersonOrm.user_id == user_id,
                    or_(
                        func.levenshtein(PersonOrm.phone, query) <= 3,  # Allowing up to 3 typos
                        PersonOrm.phone.ilike(f"%{query}%")  # Partial match
                    )
                )
            else:
                # Query both email and phone columns
                stmt = select(PersonOrm).where(
                    PersonOrm.user_id == user_id,
                    or_(
                        func.levenshtein(PersonOrm.email, query) <= 3,  # Allowing up to 3 typos
                        PersonOrm.email.ilike(f"%{query}%"),  # Partial match
                        func.levenshtein(PersonOrm.phone, query) <= 3,  # Allowing up to 3 typos
                        PersonOrm.phone.ilike(f"%{query}%")  # Partial match
                    )
                )
        elif "@" in query:
            # Query the email column
            stmt = select(PersonOrm).where(
                PersonOrm.user_id == user_id,
                or_(
                    func.levenshtein(PersonOrm.email, query) <= 3,  # Allowing up to 3 typos
                    PersonOrm.email.ilike(f"%{query}%")  # Partial match
                )
            )
        else:
            # Query the name column
            stmt = select(PersonOrm).where(
                PersonOrm.user_id == user_id,
                or_(
                    func.levenshtein(PersonOrm.name, query) <= 3,  # Allowing up to 3 typos
                    PersonOrm.name.ilike(f"%{query}%"),  # Partial match
                    func.levenshtein(PersonOrm.email, query) <= 3,  # Allowing up to 3 typos
                    PersonOrm.email.ilike(f"%{query}%")  # Partial match
                )
            )

        result = await session.execute(stmt)
        rows = result.scalars().all()
        return rows

async def search_transactions(query: str, user_id: int):
    db = Database()
    async with db.sessionmaker() as session:
        stmt = select(DealOrm).where(
            DealOrm.user_id == user_id,
            or_(
                func.levenshtein(DealOrm.name, query) <= 3,  # Allowing up to 3 typos
                DealOrm.name.ilike(f"%{query}%")  # Partial match
            )
        )
        result = await session.execute(stmt)
        rows = result.scalars().all()
        return rows

async def search_properties(query: str, user_id: int):
    db = Database()
    async with db.sessionmaker() as session:
        if any(char.isdigit() for char in query) and sum(char.isdigit() for char in query) > 6:
            # Query the mls_number column
            stmt = select(PropertyOrm).where(
                PropertyOrm.user_id == user_id,
                or_(
                    func.levenshtein(PropertyOrm.mls_number, query) <= 3,  # Allowing up to 3 typos
                    PropertyOrm.mls_number.ilike(f"%{query}%")  # Partial match
                )
            )
        else:
            # Query the address column
            stmt = select(PropertyOrm).where(
                PropertyOrm.user_id == user_id,
                or_(
                    func.levenshtein(PropertyOrm.address, query) <= 3,  # Allowing up to 3 typos
                    PropertyOrm.address.ilike(f"%{query}%")  # Partial match
                )
            )
        
        result = await session.execute(stmt)
        rows = result.scalars().all()
        return rows
