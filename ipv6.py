import random
import tkinter as tk
from tkinter import messagebox


test1 = [
    {
        "q": "V kontexte IEEE 802.15.4, čo znamená skratka CAP?",
        "options": [
            "Contention Access Period",
            "Central Access Protocol",
            "Channel Allocation Period",
            "Connection Access Point"
        ],
        "answer": "Contention Access Period"
    },
    {
        "q": "V kontexte IEEE 802.15.4, čo znamená skratka CFP?",
        "options": [
            "Contention Free Period",
            "Central Forwarding Protocol",
            "Control Frame Period",
            "Channel Free Protocol"
        ],
        "answer": "Contention Free Period"
    },
    {
        "q": "Aký je rozdiel medzi LoRa a LoRaWAN?",
        "options": [
            "LoRa je fyzická rádiová technológia, LoRaWAN je sieťový protokol",
            "LoRa je IP protokol, LoRaWAN je typ Ethernetu",
            "LoRaWAN je fyzická vrstva, LoRa je aplikačný protokol",
            "Nie je medzi nimi žiadny rozdiel"
        ],
        "answer": "LoRa je fyzická rádiová technológia, LoRaWAN je sieťový protokol"
    },
    {
        "q": "Ako sa nazývajú IPv6 adresy ekvivalentné privátnym IPv4 adresám?",
        "options": [
            "ULA — Unique Local Addresses",
            "Global Unicast Addresses",
            "Multicast Addresses",
            "Loopback Addresses"
        ],
        "answer": "ULA — Unique Local Addresses"
    },
    {
        "q": "Aký prefix majú ULA adresy v IPv6?",
        "options": [
            "fc00::/7",
            "fe80::/10",
            "ff00::/8",
            "2000::/3"
        ],
        "answer": "fc00::/7"
    },
    {
        "q": "Ktoré sú základné správy mechanizmu Neighbor Discovery v IPv6?",
        "options": [
            "RS, RA, NS, NA",
            "ARP, RARP, ICMP, TCP",
            "SYN, ACK, FIN, RST",
            "DHCP, DNS, HTTP, FTP"
        ],
        "answer": "RS, RA, NS, NA"
    },
    {
        "q": "Ako správne zapíšeme IPv6 adresu 2001:db8::1 s portom 443 v URL?",
        "options": [
            "https://[2001:db8::1]:443/",
            "https://2001:db8::1:443/",
            "https://2001:db8::1/443",
            "https://(2001:db8::1):443/"
        ],
        "answer": "https://[2001:db8::1]:443/"
    },
    {
        "q": "Aký príkaz v Cisco IOS zobrazí prehľad IPv6 adries na rozhraniach?",
        "options": [
            "show ipv6 interface brief",
            "ipconfig /all",
            "ip -6 addr",
            "show ip route"
        ],
        "answer": "show ipv6 interface brief"
    },
    {
        "q": "Aká IPv6 adresa je vyhradená pre loopback?",
        "options": [
            "::1/128",
            "fe80::1",
            "ff02::1",
            "fd00::1"
        ],
        "answer": "::1/128"
    },
    {
        "q": "Prečo sa NAT často mylne považuje za bezpečnostný mechanizmus?",
        "options": [
            "Pretože iba prekladá adresy, ale bezpečnosť zabezpečuje firewall",
            "Pretože šifruje všetky pakety",
            "Pretože blokuje všetok IPv6 traffic",
            "Pretože nahrádza antivírus"
        ],
        "answer": "Pretože iba prekladá adresy, ale bezpečnosť zabezpečuje firewall"
    },
    {
        "q": "Aký typ adresy má v IPv6 zvyčajne implicitný smerovač?",
        "options": [
            "Link-local adresa",
            "Multicast adresa",
            "Loopback adresa",
            "Broadcast adresa"
        ],
        "answer": "Link-local adresa"
    },
    {
        "q": "Aká je odporúčaná jednoduchá hodnota link-local adresy smerovača?",
        "options": [
            "fe80::1",
            "::1",
            "ff02::1",
            "fd00::1"
        ],
        "answer": "fe80::1"
    },
    {
        "q": "Koľko IP adries jednoznačne definuje statický tunel medzi dvoma smerovačmi?",
        "options": [
            "2",
            "1",
            "3",
            "4"
        ],
        "answer": "2"
    },
    {
        "q": "Aký prefix majú všetky IPv6 multicast adresy?",
        "options": [
            "ff00::/8",
            "fe80::/10",
            "fc00::/7",
            "2000::/3"
        ],
        "answer": "ff00::/8"
    },
    {
        "q": "Čo je najväčšia nevýhoda DHCPv6?",
        "options": [
            "DHCPv6 neposkytuje default gateway",
            "DHCPv6 nepodporuje IPv6 adresy",
            "DHCPv6 funguje iba cez WiFi",
            "DHCPv6 nevie priradiť DNS"
        ],
        "answer": "DHCPv6 neposkytuje default gateway"
    },
    {
        "q": "Ktorá IPv6 adresa funkčne nahrádza lokálny IPv4 broadcast?",
        "options": [
            "ff02::1",
            "::1",
            "fe80::1",
            "fd00::1"
        ],
        "answer": "ff02::1"
    },
    {
        "q": "Aká je IPv4 lokálna broadcast adresa?",
        "options": [
            "255.255.255.255",
            "127.0.0.1",
            "192.168.0.1",
            "0.0.0.0"
        ],
        "answer": "255.255.255.255"
    },
    {
        "q": "Ako je možné identifikovať zákazníkov pri Lightweight 4over?",
        "options": [
            "Pomocou IPv6 prefixu a PSID / rozsahu portov",
            "Iba pomocou MAC adresy",
            "Iba pomocou verejnej IPv4 adresy",
            "Pomocou DNS názvu"
        ],
        "answer": "Pomocou IPv6 prefixu a PSID / rozsahu portov"
    },
    {
        "q": "Ktoré technológie patria medzi IoT siete okrem WiFi?",
        "options": [
            "Zigbee a LoRaWAN",
            "HTTP a FTP",
            "TCP a UDP",
            "VGA a HDMI"
        ],
        "answer": "Zigbee a LoRaWAN"
    },
    {
        "q": "Ktoré parametre môže uzol získať z Router Advertisement?",
        "options": [
            "IPv6 prefix, prefix length, default router, MTU",
            "Iba MAC adresu",
            "Iba heslo do siete",
            "Iba verejnú IPv4 adresu"
        ],
        "answer": "IPv6 prefix, prefix length, default router, MTU"
    },
    {
        "q": "Aká je solicited-node multicast adresa pre fe80::face:b00c:baad:55?",
        "options": [
            "ff02::1:ffad:55",
            "ff02::1",
            "fe80::1:ffad:55",
            "ff00::55"
        ],
        "answer": "ff02::1:ffad:55"
    },
    {
        "q": "Môže sa viac klientov naraz pripojiť na jeden port servera cez Socket API?",
        "options": [
            "Áno, každé TCP spojenie je jednoznačné podľa IP adries a portov",
            "Nie, jeden port môže používať iba jeden klient",
            "Áno, ale iba pri UDP",
            "Nie, Socket API to nepodporuje"
        ],
        "answer": "Áno, každé TCP spojenie je jednoznačné podľa IP adries a portov"
    },
    {
        "q": "Ktoré sú základné typy NATu?",
        "options": [
            "Static NAT, Dynamic NAT, PAT/NAPT",
            "HTTP NAT, TCP NAT, UDP NAT",
            "Local NAT, Global NAT, WiFi NAT",
            "IPv4 NAT, IPv5 NAT, IPv7 NAT"
        ],
        "answer": "Static NAT, Dynamic NAT, PAT/NAPT"
    },
    {
        "q": "Na čo slúži zone index pri pingovaní link-local IPv6 adresy?",
        "options": [
            "Určuje sieťové rozhranie, cez ktoré sa má paket poslať",
            "Určuje číslo portu",
            "Určuje DNS server",
            "Určuje VLAN ID"
        ],
        "answer": "Určuje sieťové rozhranie, cez ktoré sa má paket poslať"
    }
]


test2 = [
    {
        "q": "Ako sa nazýva údaj zapisovaný za IPv6 adresou oddelený znakom %?",
        "options": [
            "Zone index alebo Scope ID",
            "Port number",
            "Subnet mask",
            "DNS suffix"
        ],
        "answer": "Zone index alebo Scope ID"
    },
    {
        "q": "Adresa začína prefixom fc::. O aký typ adresy ide?",
        "options": [
            "ULA — Unique Local Address",
            "Link-local address",
            "Multicast address",
            "Loopback address"
        ],
        "answer": "ULA — Unique Local Address"
    },
    {
        "q": "Ako správne zapíšeme fd00::1 s portom 8080 ako URL?",
        "options": [
            "http://[fd00::1]:8080/",
            "http://fd00::1:8080/",
            "http://fd00::1/8080",
            "http://(fd00::1):8080/"
        ],
        "answer": "http://[fd00::1]:8080/"
    },
    {
        "q": "Akým príkazom Cisco IOS zobrazíme tabuľku rozhraní s IPv6 adresami?",
        "options": [
            "show ipv6 interface brief",
            "show running-config",
            "ip -6 addr",
            "netstat -rn"
        ],
        "answer": "show ipv6 interface brief"
    },
    {
        "q": "Ktoré dva najdôležitejšie parametre získajú uzly z Router Advertisement?",
        "options": [
            "IPv6 prefix a default router",
            "MAC adresa a heslo",
            "Port a hostname",
            "IPv4 adresa a NAT tabuľka"
        ],
        "answer": "IPv6 prefix a default router"
    },
    {
        "q": "Aká je minimálna MTU požadovaná špecifikáciou IPv6?",
        "options": [
            "1280 bajtov",
            "576 bajtov",
            "1500 bajtov",
            "64 bajtov"
        ],
        "answer": "1280 bajtov"
    },
    {
        "q": "Aká je zdrojová IPv4 adresa paketu prichádzajúceho do Internetu od uzla za NAT?",
        "options": [
            "Verejná IPv4 adresa NAT routera",
            "Súkromná IPv4 adresa klienta",
            "Loopback adresa",
            "Multicast adresa"
        ],
        "answer": "Verejná IPv4 adresa NAT routera"
    },
    {
        "q": "Vymenujte mechanizmy spätnej kompatibility medzi IPv4 a IPv6.",
        "options": [
            "Dual Stack, Tunneling, Translation",
            "HTTP, DNS, FTP",
            "ARP, RARP, NAT",
            "VLAN, STP, DHCP"
        ],
        "answer": "Dual Stack, Tunneling, Translation"
    },
    {
        "q": "Akú špeciálnu adresu predstavuje 0:0:0:0:0:0:0:1?",
        "options": [
            "::1, teda loopback",
            "ff02::1, multicast",
            "fe80::1, link-local router",
            "fd00::1, ULA"
        ],
        "answer": "::1, teda loopback"
    },
    {
        "q": "Ak má rozhranie interface ID 1:2:3::1, aká bude link-local adresa?",
        "options": [
            "fe80::1:2:3:1",
            "ff02::1:2:3:1",
            "fd00::1:2:3:1",
            "::1"
        ],
        "answer": "fe80::1:2:3:1"
    },
    {
        "q": "Ktorú voľbu DHCPv6 nesie default route?",
        "options": [
            "Žiadnu, DHCPv6 neposkytuje default gateway",
            "Option 3",
            "Option 6",
            "Option 53"
        ],
        "answer": "Žiadnu, DHCPv6 neposkytuje default gateway"
    },
    {
        "q": "Ako sa mapujú IPv6 multicast adresy na MAC adresy?",
        "options": [
            "MAC začína 33:33 a pridajú sa posledné 32 bity IPv6 multicast adresy",
            "MAC začína ff:ff a pridajú sa prvé 32 bity IPv6 adresy",
            "Používa sa ARP",
            "Používa sa vždy MAC 00:00:00:00:00:00"
        ],
        "answer": "MAC začína 33:33 a pridajú sa posledné 32 bity IPv6 multicast adresy"
    },
    {
        "q": "Aká je solicited-node multicast adresa pre fe80::a:baba?",
        "options": [
            "ff02::1:ff0a:baba",
            "ff02::1",
            "fe80::a:baba",
            "ff00::baba"
        ],
        "answer": "ff02::1:ff0a:baba"
    },
    {
        "q": "Koľko IP adries jednoznačne definuje statický tunel medzi dvoma smerovačmi?",
        "options": [
            "2",
            "1",
            "4",
            "8"
        ],
        "answer": "2"
    },
    {
        "q": "Aký typ adresy má implicitný smerovač pri SLAAC?",
        "options": [
            "Link-local adresa",
            "Broadcast adresa",
            "Loopback adresa",
            "Anycast adresa"
        ],
        "answer": "Link-local adresa"
    },
    {
        "q": "Čo je hlavnou nevýhodou DHCPv6?",
        "options": [
            "Neposkytuje adresu predvolenej brány",
            "Nepodporuje DNS",
            "Funguje iba s IPv4",
            "Nevie priradiť IPv6 adresu"
        ],
        "answer": "Neposkytuje adresu predvolenej brány"
    },
    {
        "q": "Ktorý základný príkaz v Cisco IOS zapne posielanie Router Advertisement?",
        "options": [
            "ipv6 unicast-routing",
            "ip routing",
            "router ospf",
            "enable ipv6 dns"
        ],
        "answer": "ipv6 unicast-routing"
    },
    {
        "q": "Ktorý štandard alebo protokol patrí medzi bezdrôtové IoT siete okrem WiFi?",
        "options": [
            "Zigbee",
            "HTTP",
            "Ethernet",
            "HDMI"
        ],
        "answer": "Zigbee"
    },
    {
        "q": "Ktoré systémové volania používa TCP server v Socket API?",
        "options": [
            "socket(), bind(), listen(), accept(), recv(), send(), close()",
            "open(), read(), print(), scan()",
            "connect(), browse(), ping(), route()",
            "start(), stop(), pause(), resume()"
        ],
        "answer": "socket(), bind(), listen(), accept(), recv(), send(), close()"
    },
    {
        "q": "Aký je protokolový zásobník pre HTTP komunikáciu vo VLAN LAN sieti?",
        "options": [
            "HTTP → TCP → IP → Ethernet 802.1Q VLAN → fyzická vrstva",
            "HTTP → IP → TCP → VLAN → DNS",
            "TCP → HTTP → Ethernet → IP",
            "VLAN → HTTP → ARP → TCP"
        ],
        "answer": "HTTP → TCP → IP → Ethernet 802.1Q VLAN → fyzická vrstva"
    }
]


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IPv6 Quiz")
        self.root.geometry("850x600")
        self.root.resizable(False, False)

        self.questions = []
        self.current_question = 0
        self.score = 0
        self.results = []
        self.selected_answer = tk.StringVar()

        self.show_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()

        title = tk.Label(
            self.root,
            text="IPv6 a Internet vecí",
            font=("Arial", 26, "bold")
        )
        title.pack(pady=40)

        subtitle = tk.Label(
            self.root,
            text="Vyber test:",
            font=("Arial", 17)
        )
        subtitle.pack(pady=10)

        tk.Button(
            self.root,
            text="1 - Test 1: 24 otázok",
            font=("Arial", 15),
            width=35,
            height=2,
            command=lambda: self.start_quiz(test1)
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="2 - Test 2: 20 otázok",
            font=("Arial", 15),
            width=35,
            height=2,
            command=lambda: self.start_quiz(test2)
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="3 - Mix: 44 otázok",
            font=("Arial", 15),
            width=35,
            height=2,
            command=lambda: self.start_quiz(test1 + test2)
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Koniec",
            font=("Arial", 15),
            width=35,
            height=2,
            command=self.root.quit
        ).pack(pady=25)

    def start_quiz(self, questions):
        self.questions = questions.copy()
        random.shuffle(self.questions)

        self.current_question = 0
        self.score = 0
        self.results = []

        self.show_question()

    def show_question(self):
        self.clear_window()
        self.selected_answer.set("")

        question_data = self.questions[self.current_question]

        top_label = tk.Label(
            self.root,
            text=f"Otázka {self.current_question + 1}/{len(self.questions)}",
            font=("Arial", 16, "bold")
        )
        top_label.pack(pady=15)

        question_label = tk.Label(
            self.root,
            text=question_data["q"],
            font=("Arial", 14),
            wraplength=760,
            justify="center"
        )
        question_label.pack(pady=20)

        options = question_data["options"].copy()
        random.shuffle(options)

        for option in options:
            radio = tk.Radiobutton(
                self.root,
                text=option,
                variable=self.selected_answer,
                value=option,
                font=("Arial", 12),
                wraplength=730,
                justify="left",
                anchor="w"
            )
            radio.pack(anchor="w", padx=70, pady=6)

        tk.Button(
            self.root,
            text="Ďalej",
            font=("Arial", 14),
            width=20,
            command=self.check_answer
        ).pack(pady=30)

        tk.Button(
            self.root,
            text="Späť do menu",
            font=("Arial", 12),
            command=self.show_main_menu
        ).pack()

    def check_answer(self):
        if self.selected_answer.get() == "":
            messagebox.showwarning("Pozor", "Vyber jednu odpoveď.")
            return

        question_data = self.questions[self.current_question]

        user_answer = self.selected_answer.get()
        correct_answer = question_data["answer"]
        is_correct = user_answer == correct_answer

        if is_correct:
            self.score += 1

        self.results.append({
            "question": question_data["q"],
            "your_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

        self.current_question += 1

        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        self.clear_window()

        total = len(self.questions)
        wrong = total - self.score
        percent = self.score / total * 100

        tk.Label(
            self.root,
            text="Výsledok testu",
            font=("Arial", 26, "bold")
        ).pack(pady=30)

        result_text = (
            f"Správne odpovede: {self.score}/{total}\n"
            f"Nesprávne odpovede: {wrong}/{total}\n"
            f"Percentá: {percent:.2f}%"
        )

        tk.Label(
            self.root,
            text=result_text,
            font=("Arial", 17)
        ).pack(pady=20)

        if percent >= 90:
            mark = "Výborne!"
        elif percent >= 75:
            mark = "Dobré, ale ešte si to zopakuj."
        elif percent >= 50:
            mark = "Nie zlé, ale treba viac trénovať."
        else:
            mark = "Treba sa ešte učiť."

        tk.Label(
            self.root,
            text=mark,
            font=("Arial", 17, "bold")
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Pozrieť všetky odpovede",
            font=("Arial", 14),
            width=35,
            command=self.show_all_answers
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Pozrieť iba nesprávne odpovede",
            font=("Arial", 14),
            width=35,
            command=self.show_wrong_answers
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Späť do hlavného menu",
            font=("Arial", 14),
            width=35,
            command=self.show_main_menu
        ).pack(pady=20)

    def show_all_answers(self):
        self.show_answers_window(self.results, "Všetky odpovede")

    def show_wrong_answers(self):
        wrong_answers = [r for r in self.results if not r["is_correct"]]

        if not wrong_answers:
            messagebox.showinfo("Výborne", "Nemáš žiadne nesprávne odpovede.")
            return

        self.show_answers_window(wrong_answers, "Nesprávne odpovede")

    def show_answers_window(self, answers, title_text):
        answer_window = tk.Toplevel(self.root)
        answer_window.title(title_text)
        answer_window.geometry("900x650")

        frame = tk.Frame(answer_window)
        frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, result in enumerate(answers, start=1):
            status = "SPRÁVNE" if result["is_correct"] else "NESPRÁVNE"

            text = (
                f"{i}. {result['question']}\n\n"
                f"Stav: {status}\n"
                f"Tvoja odpoveď: {result['your_answer']}\n"
                f"Správna odpoveď: {result['correct_answer']}\n"
            )

            label = tk.Label(
                scrollable_frame,
                text=text,
                font=("Arial", 11),
                wraplength=820,
                justify="left",
                anchor="w"
            )
            label.pack(anchor="w", padx=15, pady=10)

            line = tk.Frame(scrollable_frame, height=1, bg="gray")
            line.pack(fill="x", padx=10, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()