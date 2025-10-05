from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker
from sqlalchemy import String, create_engine, Integer

engine = create_engine("sqlite:///example.db", echo=True)

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200))

    def __repr__(self):
        return f"<Item(id={self.id}, name={self.name}, description={self.description})>"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def create_itemDb(name: str, description: str):
    new_item = Item(name=name, description=description)
    session.add(new_item)
    session.commit()
    return new_item

def get_all_items():
    return session.query(Item).all()

def get_item(item_id: int):
    return session.query(Item).filter(Item.id == item_id).first()

def update_item(item_id: int, name: str, description: str):
    item = session.query(Item).filter(Item.id == item_id).first()
    if item:
        item.name = name
        item.description = description
        session.commit()
        return item
    return None

def delete_item(item_id: int):
    item = session.query(Item).filter(Item.id == item_id).first()
    if item:
        session.delete(item)
        session.commit()
        return True
    return False

def delete_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return "Database reset successfully"


print(get_all_items())