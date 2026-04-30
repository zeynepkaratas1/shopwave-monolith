import requests
import time

URL = "http://localhost:8080/actuator/health"

REQUEST_TIMEOUT = 2  # saniye (timeout)
DEADLINE = 5         # saniye (toplam süre)

latencies = []
errors = 0

start_deadline = time.time()

print("Latency/Jitter + Timeout/Deadline testi başlıyor...\n")

for i in range(10):

    # deadline kontrolü
    if time.time() - start_deadline > DEADLINE:
        print("\nDeadline aşıldı! Test durduruldu.")
        break

    try:
        start = time.time()

        response = requests.get(URL, timeout=REQUEST_TIMEOUT)

        end = time.time()

        latency = (end - start) * 1000
        latencies.append(latency)

        print(f"{i+1}. istek: {latency:.2f} ms | Status: {response.status_code}")

    except requests.exceptions.Timeout:
        errors += 1
        print(f"{i+1}. istek: TIMEOUT ❌")

    except Exception as e:
        errors += 1
        print(f"{i+1}. istek: HATA ❌ -> {e}")

# sonuçlar
if len(latencies) > 1:
    avg_latency = sum(latencies) / len(latencies)

    jitters = []
    for i in range(1, len(latencies)):
        jitters.append(abs(latencies[i] - latencies[i-1]))

    avg_jitter = sum(jitters) / len(jitters)

    print("\n--- SONUÇLAR ---")
    print(f"Ortalama Latency: {avg_latency:.2f} ms")
    print(f"Ortalama Jitter: {avg_jitter:.2f} ms")
    print(f"Hata sayısı: {errors}")
else:
    print("Yeterli veri yok")