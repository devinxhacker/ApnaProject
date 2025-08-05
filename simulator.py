import threading
import queue
import time

class RouterThread(threading.Thread):
    def __init__(self, router_obj):
        super().__init__()
        self.router = router_obj
        self.inbox = queue.Queue() # IPC mechanism [cite: 89]
        self.stop_event = threading.Event()
        self.log = [] # [cite: 92]

    def run(self):
        self.log.append(f"{time.time()}: Powering ON.")
        # Day-1 Simulation: OSPF Discovery [cite: 16, 78]
        time.sleep(1) # Stagger startup
        self.log.append(f"{time.time()}: Starting OSPF discovery...")
        # (In a real scenario, this would be a loop sending hello packets)

        while not self.stop_event.is_set():
            try:
                message = self.inbox.get(timeout=1)
                self.log.append(f"{time.time()}: Received message: {message}")
                # Process message (e.g., link failure notification)
                if message.get("type") == "LINK_FAILURE":
                    self.log.append(f"CRITICAL: Detected failure on link to {message['neighbor']}. Recalculating routes.")
            except queue.Empty:
                continue # No messages

    def stop(self):
        self.stop_event.set()

class Simulation:
    def __init__(self, routers, links):
        self.routers = {r.hostname: r for r in routers}
        self.links = links
        self.threads = {}

    def start(self):
        """Use multithreading to represent routers and switches [cite: 86]"""
        for r_name, router_obj in self.routers.items():
            thread = RouterThread(router_obj)
            self.threads[r_name] = thread
            thread.start()
        print("Simulation started. All router threads are running.")

    def stop(self):
        for thread in self.threads.values():
            thread.stop()
        print("Simulation stopped.")

    def get_logs(self, router_name):
        return self.threads[router_name].log

    def inject_link_failure(self, router1_name, router2_name):
        """Simulate a link failure and its impact [cite: 17, 80]"""
        print(f"\n--- INJECTING FAULT: Failing link between {router1_name} and {router2_name} ---")
        # Send a message to both routers about the failure
        msg1 = {"type": "LINK_FAILURE", "neighbor": router2_name}
        msg2 = {"type": "LINK_FAILURE", "neighbor": router1_name}
        self.threads[router1_name].inbox.put(msg1)
        self.threads[router2_name].inbox.put(msg2)