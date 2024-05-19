# core/utils/search.py
from sqlalchemy import select, or_
from sqlalchemy.orm import load_only
from sqlalchemy.sql.expression import func

from core.database import Databasefrom core.models import *

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
                stmt = select(PersonRowOrm).where(
                    PersonRowOrm.user_id == user_id,
                    or_(
                        func.levenshtein(PersonRowOrm.phone, query) <= 3,  # Allowing up to 3 typos
                        PersonRowOrm.phone.ilike(f"%{query}%")  # Partial match
                    )
                )
            else:
                # Query both email and phone columns
                stmt = select(PersonRowOrm).where(
                    PersonRowOrm.user_id == user_id,
                    or_(
                        func.levenshtein(PersonRowOrm.email, query) <= 3,  # Allowing up to 3 typos
                        PersonRowOrm.email.ilike(f"%{query}%"),  # Partial match
                        func.levenshtein(PersonRowOrm.phone, query) <= 3,  # Allowing up to 3 typos
                        PersonRowOrm.phone.ilike(f"%{query}%")  # Partial match
                    )
                )
        elif "@" in query:
            # Query the email column
            stmt = select(PersonRowOrm).where(
                PersonRowOrm.user_id == user_id,
                or_(
                    func.levenshtein(PersonRowOrm.email, query) <= 3,  # Allowing up to 3 typos
                    PersonRowOrm.email.ilike(f"%{query}%")  # Partial match
                )
            )
        else:
            # Query the name column
            stmt = select(PersonRowOrm).where(
                PersonRowOrm.user_id == user_id,
                or_(
                    func.levenshtein(PersonRowOrm.name, query) <= 3,  # Allowing up to 3 typos
                    PersonRowOrm.name.ilike(f"%{query}%"),  # Partial match
                    func.levenshtein(PersonRowOrm.email, query) <= 3,  # Allowing up to 3 typos
                    PersonRowOrm.email.ilike(f"%{query}%")  # Partial match
                )
            )

        result = await session.execute(stmt)
        rows = result.scalars().all()
        return rows

async def search_transactions(query: str, user_id: int):
    db = Database()
    async with db.sessionmaker() as session:
        stmt = select(TransactionRowOrm).where(
            TransactionRowOrm.user_id == user_id,
            or_(
                func.levenshtein(TransactionRowOrm.name, query) <= 3,  # Allowing up to 3 typos
                TransactionRowOrm.name.ilike(f"%{query}%")  # Partial match
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
            stmt = select(PropertyRowOrm).where(
                PropertyRowOrm.user_id == user_id,
                or_(
                    func.levenshtein(PropertyRowOrm.mls_number, query) <= 3,  # Allowing up to 3 typos
                    PropertyRowOrm.mls_number.ilike(f"%{query}%")  # Partial match
                )
            )
        else:
            # Query the address column
            stmt = select(PropertyRowOrm).where(
                PropertyRowOrm.user_id == user_id,
                or_(
                    func.levenshtein(PropertyRowOrm.address, query) <= 3,  # Allowing up to 3 typos
                    PropertyRowOrm.address.ilike(f"%{query}%")  # Partial match
                )
            )
        
        result = await session.execute(stmt)
        rows = result.scalars().all()
        return rows
