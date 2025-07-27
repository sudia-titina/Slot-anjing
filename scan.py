import os
import shodan

SHODAN_API_KEY = os.getenv("SHODAN_KEY")
if not SHODAN_API_KEY:
    raise ValueError("SHODAN_KEY environment variable not found!")

api = shodan.Shodan(SHODAN_API_KEY)

# Kata kunci identifikasi slot/judi
slot_keywords = ["slot", "judi", "jackpot", "casino", "bet", "pragmatic", "rtp", "gacor"]

# Gunakan query yang sesuai (HTTP service, negara, port 80/443)
query = 'http country:ID'  # bisa disesuaikan

try:
    print("[+] Mencari data dari Shodan...")
    results = api.search(query, limit=1000)  # limit bisa dinaikkan

    os.makedirs("output", exist_ok=True)
    with open("output/judol_results.txt", "w", encoding="utf-8") as f:
        for match in results["matches"]:
            ip = match.get("ip_str")
            port = match.get("port")
            hostnames = match.get("hostnames", [])
            html_data = match.get("http", {}).get("html", "")
            title = match.get("http", {}).get("title", "")

            combined_text = f"{' '.join(hostnames)} {title} {html_data}".lower()

            if any(keyword in combined_text for keyword in slot_keywords):
                line = f"{ip}:{port} - {title}\n"
                f.write(line)
                print(f"[🎰] Slot site ditemukan: {line.strip()}")

    print("\n[+] Proses selesai. Hasil tersimpan di output/judol_results.txt")

except shodan.APIError as e:
    print(f"[-] Error Shodan API: {e}")
