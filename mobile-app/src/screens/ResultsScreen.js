import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';

export default function ResultsScreen({ route, navigation }) {
  const { analysisData } = route.params;

  const {
    motor_preference,
    scores_adjusted,
    capacity,
    performance,
    energy_leaks,
    correction_plan,
  } = analysisData;

  const getPreferenceColor = (pref) => {
    switch(pref.toLowerCase()) {
      case 'spinner': return '#ec4899';
      case 'glider': return '#3b82f6';
      case 'launcher': return '#10b981';
      default: return '#6b7280';
    }
  };

  return (
    <ScrollView style={styles.container}>
      {/* Motor Preference Card */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>🧬 Motor Preference</Text>
        
        <View style={[
          styles.preferenceBadge,
          { backgroundColor: getPreferenceColor(motor_preference.preference) }
        ]}>
          <Text style={styles.preferenceName}>
            {motor_preference.preference.toUpperCase()}
          </Text>
        </View>

        <View style={styles.confidenceContainer}>
          <Text style={styles.confidenceLabel}>Confidence</Text>
          <View style={styles.confidenceBar}>
            <View style={[
              styles.confidenceFill,
              { width: `${motor_preference.confidence * 100}%` }
            ]} />
          </View>
          <Text style={styles.confidenceText}>
            {(motor_preference.confidence * 100).toFixed(1)}%
          </Text>
        </View>

        <Text style={styles.description}>{motor_preference.description}</Text>

        <View style={styles.coachingSection}>
          <Text style={styles.coachingTitle}>🎯 Coaching Focus:</Text>
          <Text style={styles.coachingText}>
            {motor_preference.coaching_focus}
          </Text>
        </View>

        <View style={styles.coachingSection}>
          <Text style={styles.coachingTitle}>⚠️ Avoid:</Text>
          <Text style={styles.coachingText}>
            {motor_preference.avoid_coaching}
          </Text>
        </View>
      </View>

      {/* Adjusted Scores */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>📊 Motor-Aware Scoring</Text>

        {['ground', 'engine', 'weapon'].map(component => {
          const score = scores_adjusted[component];
          const adjustment = score.adjustment;
          
          return (
            <View key={component} style={styles.scoreRow}>
              <Text style={styles.scoreLabel}>
                {component.charAt(0).toUpperCase() + component.slice(1)}
              </Text>
              
              <View style={styles.scoreBarContainer}>
                <View style={styles.scoreBar}>
                  <View style={[
                    styles.scoreBarFill,
                    { width: `${score.adjusted}%` }
                  ]} />
                </View>
                
                <View style={styles.scoreValues}>
                  <Text style={styles.scoreValue}>
                    {score.raw} → {score.adjusted}
                  </Text>
                  {adjustment !== 0 && (
                    <View style={styles.adjustmentBadge}>
                      <Text style={styles.adjustmentText}>
                        {adjustment > 0 ? '+' : ''}{adjustment}
                      </Text>
                    </View>
                  )}
                </View>
              </View>
            </View>
          );
        })}

        <View style={styles.efficiencyContainer}>
          <Text style={styles.efficiencyLabel}>Overall Efficiency</Text>
          <Text style={styles.efficiencyValue}>
            {scores_adjusted.overall_efficiency.toFixed(1)}%
          </Text>
        </View>
      </View>

      {/* Kinetic Capacity */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>⚡ Kinetic Capacity</Text>

        <View style={styles.statsGrid}>
          <View style={styles.statBox}>
            <Text style={styles.statLabel}>Bat Speed Range</Text>
            <Text style={styles.statValue}>
              {capacity.bat_speed_range.min_mph.toFixed(1)}-{capacity.bat_speed_range.max_mph.toFixed(1)} mph
            </Text>
          </View>

          <View style={styles.statBox}>
            <Text style={styles.statLabel}>Target Capacity</Text>
            <Text style={styles.statValue}>
              {capacity.bat_speed_range.midpoint_mph.toFixed(1)} mph
            </Text>
          </View>

          <View style={styles.statBox}>
            <Text style={styles.statLabel}>Predicted</Text>
            <Text style={styles.statValue}>
              {performance.predicted_bat_speed_mph.toFixed(1)} mph
            </Text>
          </View>

          {performance.actual_bat_speed_mph && (
            <View style={styles.statBox}>
              <Text style={styles.statLabel}>Actual</Text>
              <Text style={styles.statValue}>
                {performance.actual_bat_speed_mph.toFixed(1)} mph
              </Text>
            </View>
          )}

          <View style={[styles.statBox, styles.gapBox]}>
            <Text style={styles.statLabel}>Gap to Max</Text>
            <Text style={[styles.statValue, styles.gapValue]}>
              {performance.gap_to_capacity_max_mph.toFixed(1)} mph
            </Text>
          </View>
        </View>
      </View>

      {/* Correction Plan */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>🎯 Correction Plan</Text>

        <View style={styles.timelineBadge}>
          <Text style={styles.timelineText}>
            ⏱️  {correction_plan.timeline}
          </Text>
        </View>

        {/* Issues */}
        <Text style={styles.subsectionTitle}>Issues Identified</Text>
        {correction_plan.issues.map((issue, index) => (
          <View key={index} style={[
            styles.issueCard,
            issue.priority === 'CRITICAL' && styles.issueCardCritical,
            issue.priority === 'HIGH' && styles.issueCardHigh,
          ]}>
            <View style={styles.issueHeader}>
              <Text style={styles.issueName}>
                {issue.name} [{issue.priority}]
              </Text>
              <View style={styles.issueGainBadge}>
                <Text style={styles.issueGainText}>
                  +{issue.potential_gain_mph.toFixed(1)} mph
                </Text>
              </View>
            </View>
            <Text style={styles.issueDescription}>{issue.root_cause}</Text>
          </View>
        ))}

        {/* Drills */}
        <Text style={[styles.subsectionTitle, styles.subsectionMargin]}>
          Drill Progression
        </Text>
        {correction_plan.drills.map((drill, index) => (
          <TouchableOpacity
            key={index}
            style={styles.drillCard}
            onPress={() => navigation.navigate('DrillDetail', { drill })}
          >
            <View style={styles.drillHeader}>
              <Text style={styles.drillName}>{drill.drill_name}</Text>
              <View style={styles.drillStageBadge}>
                <Text style={styles.drillStageText}>
                  {drill.stage.replace('Stage ', 'S')}
                </Text>
              </View>
            </View>
            <Text style={styles.drillDescription} numberOfLines={2}>
              {drill.description}
            </Text>
            {drill.videos && drill.videos.length > 0 && (
              <Text style={styles.drillVideos}>
                🎥 {drill.videos.length} video{drill.videos.length > 1 ? 's' : ''}
              </Text>
            )}
          </TouchableOpacity>
        ))}

        {/* Success Metrics */}
        <View style={styles.successMetricsCard}>
          <Text style={styles.subsectionTitle}>🎯 Success Metrics</Text>
          <Text style={styles.metricText}>
            Target Ground: {correction_plan.success_metrics.target_ground_score}
          </Text>
          <Text style={styles.metricText}>
            Target Engine: {correction_plan.success_metrics.target_engine_score}
          </Text>
          <Text style={styles.metricText}>
            Target Weapon: {correction_plan.success_metrics.target_weapon_score}
          </Text>
          <Text style={[styles.metricText, styles.metricHighlight]}>
            Expected Gain: +{correction_plan.success_metrics.expected_bat_speed_gain_mph.toFixed(1)} mph
          </Text>
        </View>
      </View>

      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  card: {
    backgroundColor: '#fff',
    margin: 16,
    padding: 20,
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1e3a8a',
    marginBottom: 16,
  },
  preferenceBadge: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 50,
    alignSelf: 'flex-start',
    marginBottom: 16,
  },
  preferenceName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  confidenceContainer: {
    marginBottom: 16,
  },
  confidenceLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#4b5563',
    marginBottom: 8,
  },
  confidenceBar: {
    height: 8,
    backgroundColor: '#e5e7eb',
    borderRadius: 4,
    overflow: 'hidden',
  },
  confidenceFill: {
    height: '100%',
    backgroundColor: '#10b981',
  },
  confidenceText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#10b981',
    marginTop: 4,
  },
  description: {
    fontSize: 15,
    color: '#4b5563',
    lineHeight: 22,
    marginBottom: 16,
  },
  coachingSection: {
    marginBottom: 12,
  },
  coachingTitle: {
    fontSize: 15,
    fontWeight: '600',
    color: '#1e3a8a',
    marginBottom: 6,
  },
  coachingText: {
    fontSize: 14,
    color: '#4b5563',
    lineHeight: 20,
  },
  scoreRow: {
    marginBottom: 16,
  },
  scoreLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1e3a8a',
    marginBottom: 8,
  },
  scoreBarContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  scoreBar: {
    flex: 1,
    height: 24,
    backgroundColor: '#e5e7eb',
    borderRadius: 12,
    overflow: 'hidden',
    marginRight: 12,
  },
  scoreBarFill: {
    height: '100%',
    backgroundColor: '#10b981',
  },
  scoreValues: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  scoreValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1e3a8a',
    marginRight: 8,
  },
  adjustmentBadge: {
    backgroundColor: '#d1fae5',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  adjustmentText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#059669',
  },
  efficiencyContainer: {
    marginTop: 8,
    padding: 16,
    backgroundColor: '#f0fdf4',
    borderRadius: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  efficiencyLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1e3a8a',
  },
  efficiencyValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#059669',
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -8,
  },
  statBox: {
    width: '50%',
    padding: 8,
  },
  statLabel: {
    fontSize: 12,
    color: '#6b7280',
    marginBottom: 4,
  },
  statValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1e3a8a',
  },
  gapBox: {
    backgroundColor: '#fef2f2',
    borderRadius: 8,
  },
  gapValue: {
    color: '#ef4444',
  },
  timelineBadge: {
    backgroundColor: '#dbeafe',
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderRadius: 50,
    alignSelf: 'flex-start',
    marginBottom: 20,
  },
  timelineText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1e40af',
  },
  subsectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1e3a8a',
    marginBottom: 12,
  },
  subsectionMargin: {
    marginTop: 24,
  },
  issueCard: {
    backgroundColor: '#fff7ed',
    borderLeftWidth: 4,
    borderLeftColor: '#f59e0b',
    padding: 12,
    borderRadius: 8,
    marginBottom: 12,
  },
  issueCardCritical: {
    backgroundColor: '#fef2f2',
    borderLeftColor: '#ef4444',
  },
  issueCardHigh: {
    backgroundColor: '#fff7ed',
    borderLeftColor: '#f59e0b',
  },
  issueHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  issueName: {
    flex: 1,
    fontSize: 14,
    fontWeight: '600',
    color: '#1f2937',
  },
  issueGainBadge: {
    backgroundColor: '#d1fae5',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  issueGainText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#059669',
  },
  issueDescription: {
    fontSize: 13,
    color: '#4b5563',
    lineHeight: 18,
  },
  drillCard: {
    backgroundColor: '#f9fafb',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
  },
  drillHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  drillName: {
    flex: 1,
    fontSize: 15,
    fontWeight: '600',
    color: '#1f2937',
  },
  drillStageBadge: {
    backgroundColor: '#dbeafe',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  drillStageText: {
    fontSize: 11,
    fontWeight: '600',
    color: '#1e40af',
  },
  drillDescription: {
    fontSize: 14,
    color: '#4b5563',
    lineHeight: 20,
    marginBottom: 8,
  },
  drillVideos: {
    fontSize: 13,
    color: '#3b82f6',
    fontWeight: '500',
  },
  successMetricsCard: {
    backgroundColor: '#dbeafe',
    padding: 16,
    borderRadius: 12,
    marginTop: 24,
  },
  metricText: {
    fontSize: 14,
    color: '#1e3a8a',
    marginBottom: 6,
  },
  metricHighlight: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 8,
  },
});
