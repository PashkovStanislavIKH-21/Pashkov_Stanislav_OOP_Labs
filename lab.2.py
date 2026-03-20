import asyncio
import random
import time
import networkx as nx
import matplotlib.pyplot as plt


# 2. Клас пакета
class Packet:
    def __init__(self, sender, receiver, size, protocol="TCP"):
        self.sender = sender
        self.receiver = receiver
        self.size = size
        self.protocol = protocol
        self.timestamp = time.time()


# 1. Класи вузлів
class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.connections = []
        self.stats = {"sent": 0, "received": 0, "lost": 0, "latencies": []}

    def connect(self, other_node):
        if other_node not in self.connections:
            self.connections.append(other_node)
            other_node.connections.append(self)


class Router(Node):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.is_router = True


# 3. Реалізація протоколів
class BaseProtocol:
    def __init__(self, loss_rate=0.12):  # 10-15% за умовою
        self.loss_rate = loss_rate

    async def send(self, packet, target_node):
        await asyncio.sleep(random.uniform(0.01, 0.05))  # Випадкова затримка
        if random.random() < self.loss_rate:
            return False, "lost"
        return True, "delivered"


class TCPProtocol(BaseProtocol):
    async def handle_packet(self, packet, target_node):
        success, status = await self.send(packet, target_node)
        if not success:  # TCP перевідправляє (спрощена модель)
            await asyncio.sleep(0.02)
            success, status = await self.send(packet, target_node)
        return success, status


class UDPProtocol(BaseProtocol):
    async def handle_packet(self, packet, target_node):
        return await self.send(packet, target_node)


# 4. Асинхронний механізм моделювання
async def simulate_traffic(nodes, duration=2, protocol_type="TCP"):
    protocol = TCPProtocol() if protocol_type == "TCP" else UDPProtocol()
    end_time = time.time() + duration
    total_stats = {"sent": 0, "delivered": 0, "lost": 0, "latencies": []}

    while time.time() < end_time:
        sender, receiver = random.sample(nodes, 2)
        packet = Packet(sender.node_id, receiver.node_id, random.randint(64, 1500), protocol_type)

        start_send = time.time()
        success, status = await protocol.handle_packet(packet, receiver)
        latency = time.time() - start_send

        total_stats["sent"] += 1
        if success:
            total_stats["delivered"] += 1
            total_stats["latencies"].append(latency)
        else:
            total_stats["lost"] += 1

        await asyncio.sleep(0.01)

    return total_stats


def setup_topologies():
    # Зіркова топологія
    center = Router("R7")
    star_nodes = [Node(f"S{i}") for i in range(1, 8)]
    for n in star_nodes:
        center.connect(n)
    star = [center] + star_nodes

    # Гібридна топологія, що складається з двох зіркових і одної сіткової
    r1 = Router("R7")
    r2 = Router("R9")
    r3 = Router("R11")
    r2.connect(r1)
    r2.connect(r3)
    r1.connect(r3)
    group_r1 = [Node(f"S{i}") for i in range(1, 8)]
    group_r2 = [Node(f"G{i}") for i in range(1, 8)]
    group_r3 = [Node(f"A{i}") for i in range(1, 8)]
    for n in group_r1: r1.connect(n)
    for n in group_r2: r2.connect(n)
    for n in group_r3: r3.connect(n)
    for p in range(len(group_r3)):
        for jojo in range(p + 1, len(group_r3)):
            group_r3[p].connect(group_r3[jojo])
    hybrid = [r1, r2, r3] + group_r1 + group_r2 + group_r3

    return star, hybrid


def visualize_network(nodes, title):
    G = nx.Graph()
    for node in nodes:
        for conn in node.connections:
            G.add_edge(node.node_id, conn.node_id)

    plt.figure(figsize=(8, 5))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=800, edge_color='gray')
    plt.title(title)
    plt.show()


async def main():
    star_net, hybrid_net = setup_topologies()

    print("--- Симуляція топології Зірка ---")
    star_results = await simulate_traffic(star_net)

    print("--- Симуляція Гібридної топології ---")
    hybrid_results = await simulate_traffic(hybrid_net)

    visualize_network(star_net, "Star Topology")
    visualize_network(hybrid_net, "Hybrid Topology")

    # Статистика
    for name, res in [("Star", star_results), ("Hybrid", hybrid_results)]:
        avg_latency = sum(res["latencies"]) / len(res["latencies"]) if res["latencies"] else 0
        throughput = (res["delivered"] * 1024) / 2  # Байт/сек (умовно)
        print(f"\nРезультати {name}:")
        print(f"- Втрачено пакетів: {res['lost']} ({(res['lost'] / res['sent']) * 100:.1f}%)")
        print(f"- Середня затримка: {avg_latency:.4f} сек")
        print(f"- Пропускна здатність: {throughput:.2f} bps")


if __name__ == "__main__":
    asyncio.run(main())