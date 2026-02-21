import paramiko, threading, queue, socket, sys
def check_ssh(host, port, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port=int(port), username=user, password=password, timeout=5)
        print(f"\033[92m[+] AKTIF: {host}:{port} | {user} | {password}\033[0m")
        with open('ssh_validated.log', 'a') as f: f.write(f"{host}:{port}|{user}|{password}\n")
        client.close()
    except: pass
def worker(q):
    while True:
        t = q.get(); 
        if t is None: break
        try:
            hp, u, p = t.split('|')
            h, prt = hp.split(':')
            check_ssh(h, prt, u, p)
        except: pass
        q.task_done()
def main():
    q = queue.Queue(); threads = []
    for _ in range(20):
        t = threading.Thread(target=worker, args=(q,)); t.start(); threads.append(t)
    for line in sys.stdin: q.put(line.strip())
    q.join()
    for _ in range(20): q.put(None)
    for t in threads: t.join()
if __name__ == "__main__": main()
