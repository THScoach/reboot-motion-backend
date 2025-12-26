"""
Biomechanics Visualization System
Generates professional charts for analysis reports

Part of Priority 5: Visualization System
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Dict, List, Tuple
import os
import logging

logger = logging.getLogger(__name__)


class BiomechanicsVisualizer:
    """
    Generate professional biomechanics charts
    """
    
    # Professional color scheme
    COLORS = {
        'actual': '#FF6B6B',      # Red
        'potential': '#4ECDC4',   # Teal
        'primary': '#667eea',     # Purple
        'ground': '#51CF66',      # Green
        'engine': '#FFD93D',      # Yellow
        'weapon': '#FF6B6B',      # Red
        'background': '#F8F9FA',  # Light gray
        'text': '#2C3E50'         # Dark gray
    }
    
    def __init__(self):
        # Set default styling
        plt.style.use('seaborn-v0_8-darkgrid')
        matplotlib.rcParams['font.family'] = 'sans-serif'
        matplotlib.rcParams['font.size'] = 10
    
    def generate_gap_chart(
        self,
        actual_bat_speed: float,
        potential_bat_speed: float,
        output_path: str
    ) -> str:
        """
        Generate bar chart: Actual vs Potential bat speed
        
        Returns: Path to saved chart
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(self.COLORS['background'])
        ax.set_facecolor(self.COLORS['background'])
        
        categories = ['Actual', 'Potential']
        values = [actual_bat_speed, potential_bat_speed]
        colors = [self.COLORS['actual'], self.COLORS['potential']]
        
        bars = ax.bar(categories, values, color=colors, width=0.5, edgecolor='white', linewidth=2)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f} mph',
                   ha='center', va='bottom', fontsize=14, fontweight='bold')
        
        # Add gap annotation
        gap = potential_bat_speed - actual_bat_speed
        pct_achieved = (actual_bat_speed / potential_bat_speed) * 100
        
        mid_x = 0.5
        mid_y = (actual_bat_speed + potential_bat_speed) / 2
        
        ax.annotate(
            f'Gap: {gap:.1f} mph\n({100-pct_achieved:.1f}% untapped)',
            xy=(mid_x, mid_y),
            fontsize=12,
            ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=self.COLORS['primary'], linewidth=2)
        )
        
        ax.set_ylabel('Bat Speed (mph)', fontsize=12, fontweight='bold')
        ax.set_title('Bat Speed: Actual vs Potential', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylim(0, potential_bat_speed * 1.15)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=self.COLORS['background'])
        plt.close()
        
        logger.info(f"Gap chart saved to {output_path}")
        return output_path
    
    def generate_gew_radar_chart(
        self,
        ground_score: float,
        engine_score: float,
        weapon_score: float,
        output_path: str
    ) -> str:
        """
        Generate radar chart for Ground-Engine-Weapon scores
        """
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        fig.patch.set_facecolor(self.COLORS['background'])
        
        # Data
        categories = ['Ground', 'Engine', 'Weapon']
        values = [ground_score, engine_score, weapon_score]
        
        # Number of variables
        N = len(categories)
        
        # Compute angle for each axis
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        values += values[:1]  # Complete the loop
        angles += angles[:1]
        
        # Plot
        ax.plot(angles, values, 'o-', linewidth=2, color=self.COLORS['primary'])
        ax.fill(angles, values, alpha=0.25, color=self.COLORS['primary'])
        
        # Fix axis to go in the right order
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
        
        # Set y-axis limits
        ax.set_ylim(0, 100)
        ax.set_yticks([25, 50, 75, 100])
        ax.set_yticklabels(['25', '50', '75', '100'], fontsize=10)
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Title
        ax.set_title('Component Scores (G-E-W)', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=self.COLORS['background'])
        plt.close()
        
        logger.info(f"Radar chart saved to {output_path}")
        return output_path
    
    def generate_kinematic_sequence_waterfall(
        self,
        sequence_data: Dict,
        output_path: str
    ) -> str:
        """
        Generate waterfall chart showing kinematic sequence timing
        
        sequence_data = {
            'pelvis_ms': 150,
            'torso_ms': 100,
            'arm_ms': 50,
            'hand_ms': 10,
            'contact_ms': 0
        }
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(self.COLORS['background'])
        ax.set_facecolor(self.COLORS['background'])
        
        # Data
        segments = ['Pelvis', 'Torso', 'Arm', 'Hand', 'Contact']
        times_ms = [
            sequence_data.get('pelvis_ms', 0),
            sequence_data.get('torso_ms', 0),
            sequence_data.get('arm_ms', 0),
            sequence_data.get('hand_ms', 0),
            sequence_data.get('contact_ms', 0)
        ]
        
        # Create horizontal bar chart
        colors = [self.COLORS['ground'], self.COLORS['ground'], 
                 self.COLORS['engine'], self.COLORS['weapon'], 'gray']
        
        bars = ax.barh(segments, times_ms, color=colors, edgecolor='white', linewidth=2)
        
        # Add value labels
        for i, (bar, time) in enumerate(zip(bars, times_ms)):
            width = bar.get_width()
            ax.text(width + 5, bar.get_y() + bar.get_height()/2,
                   f'{time:.0f} ms',
                   ha='left', va='center', fontsize=11, fontweight='bold')
        
        ax.set_xlabel('Time Before Contact (ms)', fontsize=12, fontweight='bold')
        ax.set_title('Kinematic Sequence Timing', fontsize=16, fontweight='bold', pad=20)
        ax.invert_xaxis()  # So contact is on right
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=self.COLORS['background'])
        plt.close()
        
        logger.info(f"Kinematic sequence chart saved to {output_path}")
        return output_path
    
    def generate_energy_distribution_pie(
        self,
        lowerhalf_pct: float,
        torso_pct: float,
        arms_pct: float,
        output_path: str
    ) -> str:
        """
        Generate pie chart for energy distribution
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_facecolor(self.COLORS['background'])
        
        # Data
        labels = ['Lower Half', 'Torso', 'Arms']
        sizes = [lowerhalf_pct, torso_pct, arms_pct]
        colors = [self.COLORS['ground'], self.COLORS['engine'], self.COLORS['weapon']]
        explode = (0.05, 0.05, 0.05)  # Explode all slices slightly
        
        # Plot
        wedges, texts, autotexts = ax.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 12, 'fontweight': 'bold'}
        )
        
        # Make percentage text white
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(14)
            autotext.set_fontweight('bold')
        
        ax.set_title('Energy Distribution', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=self.COLORS['background'])
        plt.close()
        
        logger.info(f"Energy distribution chart saved to {output_path}")
        return output_path
    
    def generate_composite_report(
        self,
        player_data: Dict,
        analysis_data: Dict,
        output_path: str
    ) -> str:
        """
        Generate single composite image with all key charts
        Similar to Reboot Motion report format
        
        player_data = {
            'name': 'Eric Williams',
            'age': 33,
            'height_inches': 68,
            'weight_lbs': 190
        }
        
        analysis_data = {
            'actual_bat_speed': 57.9,
            'potential_bat_speed': 76.0,
            'ground_score': 72,
            'engine_score': 85,
            'weapon_score': 40,
            'sequence': {'pelvis_ms': 150, ...},
            'energy': {'lowerhalf_pct': 61, ...}
        }
        """
        fig = plt.figure(figsize=(16, 12))
        fig.patch.set_facecolor(self.COLORS['background'])
        
        # Title
        fig.suptitle(
            f"{player_data['name']} - Biomechanics Analysis Report",
            fontsize=20,
            fontweight='bold',
            y=0.98
        )
        
        # Create grid: 2 rows, 3 columns
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        # 1. Gap Chart (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_gap_on_axis(ax1, analysis_data['actual_bat_speed'], analysis_data['potential_bat_speed'])
        
        # 2. Radar Chart (top middle)
        ax2 = fig.add_subplot(gs[0, 1], projection='polar')
        self._plot_radar_on_axis(ax2, analysis_data['ground_score'], 
                                 analysis_data['engine_score'], analysis_data['weapon_score'])
        
        # 3. Player Info (top right)
        ax3 = fig.add_subplot(gs[0, 2])
        self._plot_player_info_on_axis(ax3, player_data, analysis_data)
        
        # 4. Kinematic Sequence (bottom left)
        ax4 = fig.add_subplot(gs[1, 0])
        self._plot_sequence_on_axis(ax4, analysis_data.get('sequence', {}))
        
        # 5. Energy Distribution (bottom middle)
        ax5 = fig.add_subplot(gs[1, 1])
        self._plot_energy_on_axis(ax5, analysis_data.get('energy', {}))
        
        # 6. Recommendations (bottom right)
        ax6 = fig.add_subplot(gs[1, 2])
        self._plot_recommendations_on_axis(ax6, analysis_data.get('recommendations', {}))
        
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=self.COLORS['background'])
        plt.close()
        
        logger.info(f"Composite report saved to {output_path}")
        return output_path
    
    # Helper methods for composite report
    def _plot_gap_on_axis(self, ax, actual, potential):
        """Plot gap chart on existing axis"""
        categories = ['Actual', 'Potential']
        values = [actual, potential]
        colors = [self.COLORS['actual'], self.COLORS['potential']]
        
        bars = ax.bar(categories, values, color=colors, width=0.5)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        gap = potential - actual
        ax.text(0.5, (actual + potential)/2, f'Gap:\n{gap:.1f} mph',
               ha='center', va='center', fontsize=10,
               bbox=dict(boxstyle='round', facecolor='white', edgecolor=self.COLORS['primary']))
        
        ax.set_ylabel('Bat Speed (mph)', fontsize=10, fontweight='bold')
        ax.set_title('Actual vs Potential', fontsize=12, fontweight='bold')
        ax.set_facecolor(self.COLORS['background'])
    
    def _plot_radar_on_axis(self, ax, ground, engine, weapon):
        """Plot radar chart on existing axis"""
        categories = ['Ground', 'Engine', 'Weapon']
        values = [ground, engine, weapon]
        
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        values += values[:1]
        angles += angles[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2, color=self.COLORS['primary'])
        ax.fill(angles, values, alpha=0.25, color=self.COLORS['primary'])
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10, fontweight='bold')
        ax.set_ylim(0, 100)
        ax.set_title('Component Scores', fontsize=12, fontweight='bold', pad=15)
    
    def _plot_player_info_on_axis(self, ax, player_data, analysis_data):
        """Display player info as text"""
        ax.axis('off')
        
        info_text = f"""
PLAYER INFO
━━━━━━━━━━━━━━━━
Name: {player_data['name']}
Age: {player_data['age']}
Height: {player_data['height_inches']}"
Weight: {player_data['weight_lbs']} lbs

ANALYSIS SUMMARY
━━━━━━━━━━━━━━━━
Bat Speed: {analysis_data['actual_bat_speed']:.1f} mph
Potential: {analysis_data['potential_bat_speed']:.1f} mph
Gap: {analysis_data['potential_bat_speed'] - analysis_data['actual_bat_speed']:.1f} mph

Ground: {analysis_data['ground_score']}/100
Engine: {analysis_data['engine_score']}/100
Weapon: {analysis_data['weapon_score']}/100
        """
        
        ax.text(0.1, 0.9, info_text, fontsize=10, verticalalignment='top',
               family='monospace', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    def _plot_sequence_on_axis(self, ax, sequence_data):
        """Plot kinematic sequence on existing axis"""
        if not sequence_data:
            ax.text(0.5, 0.5, 'No sequence data', ha='center', va='center')
            ax.axis('off')
            return
        
        segments = ['Pelvis', 'Torso', 'Arm', 'Hand']
        times = [sequence_data.get(f'{s.lower()}_ms', 0) for s in segments]
        
        ax.barh(segments, times, color=[self.COLORS['ground'], self.COLORS['ground'],
                                       self.COLORS['engine'], self.COLORS['weapon']])
        ax.set_xlabel('Time Before Contact (ms)', fontsize=10)
        ax.set_title('Kinematic Sequence', fontsize=12, fontweight='bold')
        ax.invert_xaxis()
        ax.set_facecolor(self.COLORS['background'])
    
    def _plot_energy_on_axis(self, ax, energy_data):
        """Plot energy distribution on existing axis"""
        if not energy_data:
            ax.text(0.5, 0.5, 'No energy data', ha='center', va='center')
            ax.axis('off')
            return
        
        labels = ['Lower\nHalf', 'Torso', 'Arms']
        sizes = [energy_data.get('lowerhalf_pct', 0), 
                energy_data.get('torso_pct', 0),
                energy_data.get('arms_pct', 0)]
        colors = [self.COLORS['ground'], self.COLORS['engine'], self.COLORS['weapon']]
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                          autopct='%1.0f%%', startangle=90)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('Energy Distribution', fontsize=12, fontweight='bold')
    
    def _plot_recommendations_on_axis(self, ax, recommendations):
        """Display recommendations as text"""
        ax.axis('off')
        
        if not recommendations:
            ax.text(0.5, 0.5, 'No recommendations', ha='center', va='center')
            return
        
        rec_text = f"""
RECOMMENDATIONS
━━━━━━━━━━━━━━━━
Focus: {recommendations.get('primary_component', 'N/A')}

Estimated Gain:
+{recommendations.get('estimated_gain_mph', 0):.1f} mph

Priority:
{recommendations.get('priority', 'N/A')}

Training:
{recommendations.get('training_frequency', 'N/A')}
        """
        
        ax.text(0.1, 0.9, rec_text, fontsize=10, verticalalignment='top',
               family='monospace', bbox=dict(boxstyle='round', 
               facecolor=self.COLORS['primary'], alpha=0.2))


if __name__ == "__main__":
    # Test the visualizer
    print("="*70)
    print("BIOMECHANICS VISUALIZER TEST")
    print("="*70)
    
    viz = BiomechanicsVisualizer()
    
    # Create output directory
    os.makedirs('/tmp/test_charts', exist_ok=True)
    
    # Test data
    print("\nGenerating test charts...")
    
    # 1. Gap chart
    print("  1. Gap chart...")
    viz.generate_gap_chart(57.9, 76.0, '/tmp/test_charts/gap.png')
    
    # 2. Radar chart
    print("  2. Radar chart...")
    viz.generate_gew_radar_chart(72, 85, 40, '/tmp/test_charts/radar.png')
    
    # 3. Kinematic sequence
    print("  3. Kinematic sequence...")
    viz.generate_kinematic_sequence_waterfall(
        {'pelvis_ms': 150, 'torso_ms': 100, 'arm_ms': 50, 'hand_ms': 10, 'contact_ms': 0},
        '/tmp/test_charts/sequence.png'
    )
    
    # 4. Energy distribution
    print("  4. Energy distribution...")
    viz.generate_energy_distribution_pie(61, 29, 10, '/tmp/test_charts/energy.png')
    
    # 5. Composite report
    print("  5. Composite report...")
    player_data = {
        'name': 'Eric Williams',
        'age': 33,
        'height_inches': 68,
        'weight_lbs': 190
    }
    
    analysis_data = {
        'actual_bat_speed': 57.9,
        'potential_bat_speed': 76.0,
        'ground_score': 72,
        'engine_score': 85,
        'weapon_score': 40,
        'sequence': {
            'pelvis_ms': 150,
            'torso_ms': 100,
            'arm_ms': 50,
            'hand_ms': 10,
            'contact_ms': 0
        },
        'energy': {
            'lowerhalf_pct': 61,
            'torso_pct': 29,
            'arms_pct': 10
        },
        'recommendations': {
            'primary_component': 'WEAPON',
            'estimated_gain_mph': 7.2,
            'priority': 'CRITICAL',
            'training_frequency': '5-6 days/week'
        }
    }
    
    viz.generate_composite_report(player_data, analysis_data, '/tmp/test_charts/composite.png')
    
    print("\n✅ All charts generated successfully!")
    print("\nChart files:")
    for f in os.listdir('/tmp/test_charts'):
        size_kb = os.path.getsize(f'/tmp/test_charts/{f}') / 1024
        print(f"  - {f}: {size_kb:.1f} KB")
    
    print("\n" + "="*70)
