import asyncio
import random
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# 1. Налаштування бази даних
DATABASE_URL = "sqlite+aiosqlite:///network_nodes.db"
Base = declarative_base()


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String, nullable=False)
    status = Column(String, default="Unknown")

    def __repr__(self):
        return f"<Node(ID={self.id}, IP={self.ip_address}, Status={self.status})>"


# Створення двигуна
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# 2. Функція отримання списку вузлів
async def get_all_nodes():
    async with async_session() as session:
        result = await session.execute(select(Node))
        return result.scalars().all()


# 3. Асинхронна імітація перевірки статусу (Ping)
async def check_node_status(node_id, ip):
    await asyncio.sleep(random.uniform(0.5, 2.0))  # Імітація затримки мережі
    new_status = random.choice(["Online", "Offline", "Timeout"])
    return node_id, new_status


# 4. Система збору та оновлення статусів
async def monitor_nodes():
    nodes = await get_all_nodes()
    print(f"Починаємо моніторинг {len(nodes)} вузлів...")

    # Створюємо список завдань для одночасного виконання
    tasks = [check_node_status(node.id, node.ip_address) for node in nodes]
    results = await asyncio.gather(*tasks)

    # Оновлення даних у базі
    async with async_session() as session:
        for node_id, new_status in results:
            node = await session.get(Node, node_id)
            if node:
                node.status = new_status
        await session.commit()
    print("Моніторинг завершено, дані оновлено.\n")


# Допоміжна функція для ініціалізації даних
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        test_nodes = [
            Node(ip_address=f"192.168.1.{i}", status="Initial")
            for i in range(1, 13)  # Створюємо 12 вузлів
        ]
        session.add_all(test_nodes)
        await session.commit()


# Головний запуск
async def main():
    await init_db()

    print("Стан вузлів ПЕРЕД оновленням:")
    nodes_before = await get_all_nodes()
    for n in nodes_before: print(n)
    print("\n")

    await monitor_nodes()

    print("Стан вузлів ПІСЛЯ оновлення:")
    nodes_after = await get_all_nodes()
    for n in nodes_after: print(n)


if __name__ == "__main__":
    asyncio.run(main())