"""
Master script to generate all improved charts for scientific publication
Runs all chart generation scripts in sequence
"""

import subprocess
import sys
import os
from datetime import datetime

def run_script(script_name):
    """Run a chart generation script and report status"""
    print(f"\n{'='*70}")
    print(f"Running: {script_name}")
    print(f"{'='*70}")
    
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
        print(f"✓ {script_name} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {script_name} failed with error:")
        print(e.stdout)
        print(e.stderr)
        return False
    except Exception as e:
        print(f"✗ {script_name} failed with exception: {str(e)}")
        return False

def main():
    """Main execution function"""
    start_time = datetime.now()
    
    print("="*70)
    print("CHART GENERATION FOR SCIENTIFIC PUBLICATION - VERSION 1")
    print("="*70)
    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # List of chart scripts to run
    scripts = [
        'chart_01_event_types.py',
        'chart_02_temporal_patterns.py',
        'chart_03_hourly_distribution.py',
        'chart_04_spatial_coverage.py',
        'chart_05_hourly_by_season.py',
        'chart_06_duration_distribution.py',
        'chart_07a_duration_by_type.py',
        'chart_07b_duration_by_season.py',
        'chart_08_duration_categories.py'
    ]
    
    results = {}
    for script in scripts:
        results[script] = run_script(script)
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    successful = sum(results.values())
    total = len(results)
    
    for script, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {script}")
    
    print(f"\nTotal: {successful}/{total} charts generated successfully")
    print(f"Duration: {duration.total_seconds():.2f} seconds")
    print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if successful == total:
        print("\n✓ All charts generated successfully!")
        print(f"Charts saved to: results/charts/v1/")
        return 0
    else:
        print(f"\n✗ {total - successful} chart(s) failed to generate")
        return 1

if __name__ == '__main__':
    sys.exit(main())
