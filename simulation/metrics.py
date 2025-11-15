# simulation/metrics.py

import matplotlib.pyplot as plt
import time

class MetricsCollector:
    """Collects and analyzes simulation metrics"""
    
    def __init__(self):
        self.runs = []
        
    def add_run(self, num_agents, results, duration):
        """Add a simulation run to metrics"""
        self.runs.append({
            'num_agents': num_agents,
            'results': results,
            'duration': duration
        })
    
    def compare_agent_counts(self, maze, simulator_class, agent_counts, trials=5):
        """
        Compare performance with different numbers of agents.
        Run multiple trials for each agent count.
        """
        comparison_data = {}
        
        for num_agents in agent_counts:
            print(f"\nTesting with {num_agents} agent(s)...")
            
            trial_results = []
            
            for trial in range(trials):
                # Reset maze
                maze.generate()
                
                # Create simulator
                from config import AGENT_ENERGY, AGENT_VISION_RANGE, COMMUNICATION_RANGE
                sim = simulator_class(
                    maze,
                    num_agents,
                    AGENT_ENERGY,
                    AGENT_VISION_RANGE,
                    COMMUNICATION_RANGE
                )
                
                # Run simulation
                start_time = time.time()
                results = sim.run_until_complete(max_steps=1000)
                duration = time.time() - start_time
                
                trial_results.append({
                    'steps': results['steps'],
                    'completed': results['completed'],
                    'explored': results['total_cells_explored'],
                    'duration': duration,
                    'path_length': results['best_path_length']
                })
                
                print(f"  Trial {trial + 1}: Steps={results['steps']}, " +
                      f"Explored={results['total_cells_explored']}, " +
                      f"Completed={results['completed']}")
            
            # Calculate averages
            avg_steps = sum(r['steps'] for r in trial_results) / trials
            avg_explored = sum(r['explored'] for r in trial_results) / trials
            avg_duration = sum(r['duration'] for r in trial_results) / trials
            success_rate = sum(1 for r in trial_results if r['completed']) / trials
            
            comparison_data[num_agents] = {
                'avg_steps': avg_steps,
                'avg_explored': avg_explored,
                'avg_duration': avg_duration,
                'success_rate': success_rate,
                'trials': trial_results
            }
        
        return comparison_data
    
    def plot_comparison(self, comparison_data, save_path='comparison.png'):
        """Plot comparison charts"""
        agent_counts = sorted(comparison_data.keys())
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Multi-Agent System Performance Comparison', fontsize=16)
        
        # Steps to completion
        avg_steps = [comparison_data[n]['avg_steps'] for n in agent_counts]
        ax1.plot(agent_counts, avg_steps, marker='o', linewidth=2, markersize=8)
        ax1.set_xlabel('Number of Agents')
        ax1.set_ylabel('Average Steps to Completion')
        ax1.set_title('Efficiency: Steps vs Agent Count')
        ax1.grid(True, alpha=0.3)
        
        # Cells explored
        avg_explored = [comparison_data[n]['avg_explored'] for n in agent_counts]
        ax2.plot(agent_counts, avg_explored, marker='s', color='green', linewidth=2, markersize=8)
        ax2.set_xlabel('Number of Agents')
        ax2.set_ylabel('Average Cells Explored')
        ax2.set_title('Exploration Coverage')
        ax2.grid(True, alpha=0.3)
        
        # Success rate
        success_rates = [comparison_data[n]['success_rate'] * 100 for n in agent_counts]
        ax3.bar(agent_counts, success_rates, color='steelblue', alpha=0.7)
        ax3.set_xlabel('Number of Agents')
        ax3.set_ylabel('Success Rate (%)')
        ax3.set_title('Mission Success Rate')
        ax3.set_ylim([0, 105])
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Duration
        avg_durations = [comparison_data[n]['avg_duration'] for n in agent_counts]
        ax4.plot(agent_counts, avg_durations, marker='^', color='red', linewidth=2, markersize=8)
        ax4.set_xlabel('Number of Agents')
        ax4.set_ylabel('Average Duration (seconds)')
        ax4.set_title('Computation Time')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nComparison chart saved to: {save_path}")
        plt.show()
    
    def print_summary(self, comparison_data):
        """Print summary statistics"""
        print("\n" + "="*60)
        print("PERFORMANCE SUMMARY")
        print("="*60)
        
        for num_agents in sorted(comparison_data.keys()):
            data = comparison_data[num_agents]
            print(f"\n{num_agents} Agent(s):")
            print(f"  Average Steps:     {data['avg_steps']:.1f}")
            print(f"  Average Explored:  {data['avg_explored']:.1f}")
            print(f"  Success Rate:      {data['success_rate']*100:.1f}%")
            print(f"  Average Duration:  {data['avg_duration']:.3f}s")
        
        # Find optimal configuration
        valid_configs = {k: v for k, v in comparison_data.items() if v['success_rate'] > 0}
        if valid_configs:
            best_steps = min(valid_configs.items(), key=lambda x: x[1]['avg_steps'])
            best_speed = min(valid_configs.items(), key=lambda x: x[1]['avg_duration'])
            
            print("\n" + "-"*60)
            print("OPTIMAL CONFIGURATIONS:")
            print(f"  Fewest Steps:       {best_steps[0]} agents ({best_steps[1]['avg_steps']:.1f} steps)")
            print(f"  Fastest Execution:  {best_speed[0]} agents ({best_speed[1]['avg_duration']:.3f}s)")
        
        print("="*60)