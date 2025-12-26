"""
HTML Report Generator
Generates professional HTML reports with embedded charts

Part of Priority 5: Visualization System
"""

import os
import base64
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generate HTML reports with embedded biomechanics analysis
    """
    
    def __init__(self):
        pass
    
    def _encode_image_to_base64(self, image_path: str) -> str:
        """
        Encode image file to base64 for embedding in HTML
        
        Args:
            image_path: Path to image file
            
        Returns:
            Base64 encoded image string
        """
        try:
            with open(image_path, 'rb') as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                return f"data:image/png;base64,{encoded}"
        except Exception as e:
            logger.error(f"Failed to encode image {image_path}: {e}")
            return ""
    
    def generate_html_report(
        self,
        player_data: Dict,
        analysis_results: Dict,
        chart_paths: Dict,
        output_path: str
    ) -> str:
        """
        Generate HTML report with embedded charts
        
        Args:
            player_data: Player information
            analysis_results: Complete analysis results
            chart_paths: Dictionary of chart file paths
            output_path: Where to save HTML file
            
        Returns:
            Path to generated HTML file
        """
        # Encode charts to base64
        charts_base64 = {}
        for chart_name, chart_path in chart_paths.items():
            if os.path.exists(chart_path):
                charts_base64[chart_name] = self._encode_image_to_base64(chart_path)
        
        # Generate HTML
        html_content = self._generate_html_template(
            player_data,
            analysis_results,
            charts_base64
        )
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML report saved to {output_path}")
        return output_path
    
    def _generate_html_template(
        self,
        player_data: Dict,
        analysis: Dict,
        charts: Dict
    ) -> str:
        """Generate complete HTML report template"""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{player_data.get('name', 'Player')} - Biomechanics Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #2C3E50;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .player-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .info-card {{
            background: #F8F9FA;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        
        .info-card h3 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .info-card p {{
            font-size: 1.5em;
            font-weight: bold;
            color: #2C3E50;
        }}
        
        .chart-container {{
            margin: 30px 0;
            text-align: center;
        }}
        
        .chart-container img {{
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .chart-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 15px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .metric-card h3 {{
            font-size: 1.1em;
            margin-bottom: 10px;
            opacity: 0.9;
        }}
        
        .metric-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .metric-card .label {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .recommendations {{
            background: #FFF3CD;
            border-left: 5px solid #FFC107;
            padding: 25px;
            border-radius: 10px;
            margin-top: 30px;
        }}
        
        .recommendations h3 {{
            color: #856404;
            margin-bottom: 15px;
        }}
        
        .recommendations ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .recommendations li {{
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
        }}
        
        .footer {{
            background: #F8F9FA;
            padding: 20px;
            text-align: center;
            color: #6c757d;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{player_data.get('name', 'Player Analysis')}</h1>
            <p>Biomechanics Analysis Report</p>
        </div>
        
        <div class="content">
            <!-- Player Info Section -->
            <div class="section">
                <h2>Player Information</h2>
                <div class="player-info">
                    <div class="info-card">
                        <h3>Age</h3>
                        <p>{player_data.get('age', 'N/A')} years</p>
                    </div>
                    <div class="info-card">
                        <h3>Height</h3>
                        <p>{player_data.get('height_inches', 'N/A')}"</p>
                    </div>
                    <div class="info-card">
                        <h3>Weight</h3>
                        <p>{player_data.get('weight_lbs', 'N/A')} lbs</p>
                    </div>
                </div>
            </div>
            
            <!-- Key Metrics Section -->
            <div class="section">
                <h2>Key Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>Actual Bat Speed</h3>
                        <div class="value">{analysis.get('actual_bat_speed', 0):.1f}</div>
                        <div class="label">mph</div>
                    </div>
                    <div class="metric-card">
                        <h3>Potential Bat Speed</h3>
                        <div class="value">{analysis.get('potential_bat_speed', 0):.1f}</div>
                        <div class="label">mph</div>
                    </div>
                    <div class="metric-card">
                        <h3>Gap</h3>
                        <div class="value">{analysis.get('potential_bat_speed', 0) - analysis.get('actual_bat_speed', 0):.1f}</div>
                        <div class="label">mph untapped</div>
                    </div>
                </div>
            </div>
            
            <!-- Gap Chart -->
            {f'''
            <div class="section">
                <div class="chart-container">
                    <div class="chart-title">Bat Speed: Actual vs Potential</div>
                    <img src="{charts.get('gap', '')}" alt="Gap Chart">
                </div>
            </div>
            ''' if 'gap' in charts else ''}
            
            <!-- Component Scores Section -->
            <div class="section">
                <h2>Component Scores</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>Ground</h3>
                        <div class="value">{analysis.get('ground_score', 0)}</div>
                        <div class="label">/ 100</div>
                    </div>
                    <div class="metric-card">
                        <h3>Engine</h3>
                        <div class="value">{analysis.get('engine_score', 0)}</div>
                        <div class="label">/ 100</div>
                    </div>
                    <div class="metric-card">
                        <h3>Weapon</h3>
                        <div class="value">{analysis.get('weapon_score', 0)}</div>
                        <div class="label">/ 100</div>
                    </div>
                </div>
            </div>
            
            <!-- Radar Chart -->
            {f'''
            <div class="section">
                <div class="chart-container">
                    <div class="chart-title">Ground-Engine-Weapon Radar</div>
                    <img src="{charts.get('radar', '')}" alt="Radar Chart">
                </div>
            </div>
            ''' if 'radar' in charts else ''}
            
            <!-- Kinematic Sequence Chart -->
            {f'''
            <div class="section">
                <div class="chart-container">
                    <div class="chart-title">Kinematic Sequence Timing</div>
                    <img src="{charts.get('sequence', '')}" alt="Kinematic Sequence">
                </div>
            </div>
            ''' if 'sequence' in charts else ''}
            
            <!-- Energy Distribution Chart -->
            {f'''
            <div class="section">
                <div class="chart-container">
                    <div class="chart-title">Energy Distribution</div>
                    <img src="{charts.get('energy', '')}" alt="Energy Distribution">
                </div>
            </div>
            ''' if 'energy' in charts else ''}
            
            <!-- Composite Report -->
            {f'''
            <div class="section">
                <div class="chart-container">
                    <div class="chart-title">Complete Analysis Overview</div>
                    <img src="{charts.get('composite', '')}" alt="Composite Report">
                </div>
            </div>
            ''' if 'composite' in charts else ''}
            
            <!-- Recommendations Section -->
            {self._generate_recommendations_html(analysis.get('recommendations', {}))}
        </div>
        
        <div class="footer">
            <p>Generated by Kinetic DNA Blueprint Analysis System</p>
            <p>© 2024 Reboot Motion Backend</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_recommendations_html(self, recommendations: Dict) -> str:
        """Generate recommendations section HTML"""
        if not recommendations:
            return ""
        
        return f"""
            <div class="section">
                <h2>Recommendations</h2>
                <div class="recommendations">
                    <h3>🎯 Primary Focus: {recommendations.get('primary_component', 'N/A')}</h3>
                    <p><strong>Priority:</strong> {recommendations.get('priority', 'N/A')}</p>
                    <p><strong>Estimated Gain:</strong> +{recommendations.get('estimated_gain_mph', 0):.1f} mph</p>
                    <p><strong>Training Frequency:</strong> {recommendations.get('training_frequency', 'N/A')}</p>
                    
                    {self._generate_drills_html(recommendations.get('drills', []))}
                </div>
            </div>
        """
    
    def _generate_drills_html(self, drills: list) -> str:
        """Generate drills list HTML"""
        if not drills:
            return ""
        
        drills_html = "<h4>Recommended Drills:</h4><ul>"
        for drill in drills:
            drills_html += f"<li>{drill}</li>"
        drills_html += "</ul>"
        
        return drills_html


if __name__ == "__main__":
    # Test the report generator
    print("="*70)
    print("HTML REPORT GENERATOR TEST")
    print("="*70)
    
    generator = ReportGenerator()
    
    # Test data
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
        'recommendations': {
            'primary_component': 'WEAPON',
            'priority': 'CRITICAL',
            'estimated_gain_mph': 7.2,
            'training_frequency': '5-6 days/week',
            'drills': [
                'Tee work focusing on hand path',
                'Inside-out swing path drills',
                'Barrel control exercises'
            ]
        }
    }
    
    chart_paths = {
        'gap': '/home/user/webapp/charts/eric_williams/gap.png',
        'radar': '/home/user/webapp/charts/eric_williams/radar.png',
        'sequence': '/home/user/webapp/charts/eric_williams/sequence.png',
        'energy': '/home/user/webapp/charts/eric_williams/energy.png',
        'composite': '/home/user/webapp/charts/eric_williams/composite_report.png'
    }
    
    # Generate report
    output_path = '/home/user/webapp/reports/eric_williams_report.html'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    generator.generate_html_report(player_data, analysis_data, chart_paths, output_path)
    
    print(f"\n✅ HTML report generated: {output_path}")
    
    # Check file size
    size_kb = os.path.getsize(output_path) / 1024
    print(f"   File size: {size_kb:.1f} KB")
    
    print("\n" + "="*70)
