import requests
import time

URL = "http://localhost:8080/actuator/health"
latencies = []

print("Latency/Jitter testi başlıyor...\n")

for i in range(10):
    start = time.time()
    response = requests.get(URL)
    end = time.time()

    latency_ms = (end - start) * 1000
    latencies.append(latency_ms)

    print(f"{i + 1}. istek latency: {latency_ms:.2f} ms | Status: {response.status_code}")

avg_latency = sum(latencies) / len(latencies)

jitters = []
for i in range(1, len(latencies)):
    jitters.append(abs(latencies[i] - latencies[i - 1]))

avg_jitter = sum(jitters) / len(jitters)

print("\n--- SONUÇLAR ---")
print(f"Ortalama Latency: {avg_latency:.2f} ms")
print(f"Ortalama Jitter: {avg_jitter:.2f} ms")