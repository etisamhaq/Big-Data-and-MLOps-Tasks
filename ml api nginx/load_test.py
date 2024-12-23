import requests
import time
import psutil
import docker
import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import seaborn as sns
from datetime import datetime

class LoadTester:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.containers = {
            'nginx': 'nginx_lb',
            'api1': 'ml_api_1',
            'api2': 'ml_api_2'
        }
        self.metrics = {
            'timestamp': [],
            'container': [],
            'cpu_usage': [],
            'memory_usage': [],
            'response_time': []
        }

    def make_request(self):
        start_time = time.time()
        try:
            response = requests.post(
                'http://localhost/predict',
                json={"features": [5.1, 3.5, 1.4, 0.2]},
                headers={"Content-Type": "application/json"}
            )
            response_time = time.time() - start_time
            return response_time
        except Exception as e:
            print(f"Request failed: {e}")
            return None

    def collect_container_metrics(self):
        timestamp = datetime.now()
        for name, container_name in self.containers.items():
            try:
                container = self.docker_client.containers.get(container_name)
                stats = container.stats(stream=False)
                
                # Calculate CPU usage
                cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                           stats['precpu_stats']['cpu_usage']['total_usage']
                system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                             stats['precpu_stats']['system_cpu_usage']
                cpu_usage = (cpu_delta / system_delta) * 100.0

                # Calculate memory usage (in MB)
                memory_usage = stats['memory_stats']['usage'] / (1024 * 1024)

                self.metrics['timestamp'].append(timestamp)
                self.metrics['container'].append(name)
                self.metrics['cpu_usage'].append(cpu_usage)
                self.metrics['memory_usage'].append(memory_usage)
                self.metrics['response_time'].append(None)
            except Exception as e:
                print(f"Error collecting metrics for {name}: {e}")

    def run_load_test(self, num_requests=20, concurrent_requests=4):
        print(f"Starting load test with {num_requests} requests ({concurrent_requests} concurrent)...")
        
        with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            for _ in range(num_requests):
                response_time = executor.submit(self.make_request).result()
                if response_time:
                    self.metrics['timestamp'].append(datetime.now())
                    self.metrics['container'].append('request')
                    self.metrics['cpu_usage'].append(None)
                    self.metrics['memory_usage'].append(None)
                    self.metrics['response_time'].append(response_time)
                self.collect_container_metrics()
                time.sleep(0.1)  # Small delay between requests

    def generate_report(self):
        # Convert metrics to DataFrame
        df = pd.DataFrame(self.metrics)
        
        # Create plots
        plt.style.use('default')
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))

        # CPU Usage Plot
        cpu_df = df[df['cpu_usage'].notna()]
        sns.lineplot(data=cpu_df, x=cpu_df.index, y='cpu_usage', hue='container', ax=ax1)
        ax1.set_title('CPU Usage Over Time')
        ax1.set_ylabel('CPU Usage (%)')

        # Memory Usage Plot
        mem_df = df[df['memory_usage'].notna()]
        sns.lineplot(data=mem_df, x=mem_df.index, y='memory_usage', hue='container', ax=ax2)
        ax2.set_title('Memory Usage Over Time')
        ax2.set_ylabel('Memory Usage (MB)')

        # Response Time Plot
        resp_df = df[df['response_time'].notna()]
        sns.histplot(data=resp_df, x='response_time', bins=30, ax=ax3)
        ax3.set_title('Response Time Distribution')
        ax3.set_xlabel('Response Time (seconds)')

        plt.tight_layout()
        plt.savefig('performance_report.png')
        print("Performance report saved as 'performance_report.png'")

        # Generate summary statistics
        summary = {
            'CPU Usage (%)': cpu_df.groupby('container')['cpu_usage'].describe(),
            'Memory Usage (MB)': mem_df.groupby('container')['memory_usage'].describe(),
            'Response Time (s)': resp_df['response_time'].describe()
        }

        # Save summary to CSV
        with open('performance_summary.txt', 'w') as f:
            f.write("Performance Test Summary\n")
            f.write("=======================\n\n")
            for metric, stats in summary.items():
                f.write(f"{metric}:\n")
                f.write(str(stats))
                f.write("\n\n")
        print("Performance summary saved as 'performance_summary.txt'")

if __name__ == "__main__":
    # Install required packages
    # pip install requests docker pandas matplotlib seaborn psutil

    tester = LoadTester()
    tester.run_load_test(num_requests=20, concurrent_requests=4)
    tester.generate_report() 