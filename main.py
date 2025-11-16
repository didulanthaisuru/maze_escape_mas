#!/usr/bin/env python3
# main.py - Main entry point for Multi-Agent Maze Escape Simulation

import sys
import argparse
from environment.maze import Maze
from simulation.simulator import Simulator
from visualization.renderer import Renderer
from simulation.metrics import MetricsCollector
import config

def run_visualization_mode(args):
    """Run simulation with pygame visualization"""
    print("Starting Multi-Agent Maze Escape Simulation...")
    print(f"Maze Size: {config.MAZE_WIDTH}x{config.MAZE_HEIGHT}")
    print(f"Max Steps: {config.MAX_STEPS}")
    print(f"Using: {'Fixed Maze' if not args.random_maze else 'Random Maze'}\n")
    
    # Create maze (fixed by default for better reliability)
    maze = Maze(config.MAZE_WIDTH, config.MAZE_HEIGHT, config.WALL_DENSITY, 
                use_fixed_maze=not args.random_maze)
    maze.generate()
    print("Maze generated successfully!")
    print(f"Start: {maze.start_pos}, Exit: {maze.exit_pos}\n")
    
    # Create initial simulator with default number of agents
    simulator = Simulator(
        maze,
        config.NUM_AGENTS,
        config.AGENT_ENERGY,
        config.AGENT_VISION_RANGE,
        config.COMMUNICATION_RANGE
    )
    
    # Create renderer - it will handle agent selection on startup
    renderer = Renderer(maze, simulator)
    
    # Show agent selection first
    renderer.selecting_agents = True
    renderer.paused = True
    
    print("Select number of agents to start...")
    print("Controls:")
    print("  ESC or Close Window: Exit")
    print("  R: Reset and select agents again")
    print("  M: New Maze (regenerate maze)")
    print("  SPACE: Pause/Unpause\n")
    
    # Run renderer
    results = renderer.run(max_steps=config.MAX_STEPS)
    
    # Print results
    print("\n" + "="*60)
    print("SIMULATION RESULTS")
    print("="*60)
    print(f"Total Steps: {results['steps']}")
    print(f"Completed: {results['completed']}")
    print(f"Winner: Agent {results['winner']}" if results['winner'] is not None else "No winner")
    print(f"Agents Reached Exit: {results['agents_reached_exit']}")
    print(f"Total Cells Explored: {results['total_cells_explored']}")
    print(f"Dead Ends Found: {results['dead_ends_found']}")
    print(f"Best Path Length: {results['best_path_length']}")
    print("="*60)
    
    return results

def run_benchmark_mode(args):
    """Run performance benchmark comparing different agent counts"""
    print("Running Performance Benchmark...")
    print("This will test multiple agent configurations\n")
    
    # Create maze (use fixed maze for consistent benchmarking)
    maze = Maze(config.MAZE_WIDTH, config.MAZE_HEIGHT, config.WALL_DENSITY, 
                use_fixed_maze=not args.random_maze)
    
    # Create metrics collector
    metrics = MetricsCollector()
    
    # Test different agent counts
    agent_counts = args.agents if args.agents else [1, 2, 3, 5, 7]
    trials = args.trials if args.trials else 5
    
    print(f"Agent counts to test: {agent_counts}")
    print(f"Trials per configuration: {trials}")
    print(f"Using: {'Fixed Maze' if not args.random_maze else 'Random Maze'}\n")
    
    # Run comparison
    comparison_data = metrics.compare_agent_counts(
        maze,
        Simulator,
        agent_counts,
        trials=trials
    )
    
    # Print summary
    metrics.print_summary(comparison_data)
    
    # Plot results
    if not args.no_plot:
        metrics.plot_comparison(comparison_data, save_path='performance_comparison.png')
    
    return comparison_data

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Multi-Agent Maze Escape Simulation'
    )
    
    parser.add_argument(
        '--mode',
        choices=['visual', 'benchmark'],
        default='visual',
        help='Run mode: visual (pygame) or benchmark (performance testing)'
    )
    
    parser.add_argument(
        '--agents',
        type=int,
        nargs='+',
        help='Agent counts to test in benchmark mode (e.g., --agents 1 3 5)'
    )
    
    parser.add_argument(
        '--trials',
        type=int,
        default=5,
        help='Number of trials per configuration in benchmark mode'
    )
    
    parser.add_argument(
        '--no-plot',
        action='store_true',
        help='Disable plotting in benchmark mode'
    )
    
    parser.add_argument(
        '--random-maze',
        action='store_true',
        help='Use random maze generation instead of fixed maze (may be unsolvable)'
    )
    
    args = parser.parse_args()
    
    try:
        if args.mode == 'visual':
            run_visualization_mode(args)
        elif args.mode == 'benchmark':
            run_benchmark_mode(args)
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()