import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Linking,
} from 'react-native';
import { incrementVideoView } from '../services/api';

export default function DrillDetailScreen({ route }) {
  const { drill } = route.params;

  const handleVideoPress = async (video) => {
    try {
      await incrementVideoView(video.video_id);
      await Linking.openURL(video.source_url);
    } catch (error) {
      console.error('Error opening video:', error);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        {/* Header */}
        <View style={styles.stageBadge}>
          <Text style={styles.stageText}>{drill.stage}</Text>
        </View>

        <Text style={styles.title}>{drill.drill_name}</Text>
        <Text style={styles.description}>{drill.description}</Text>

        {/* How It Works */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>⚙️ How It Works</Text>
          <Text style={styles.sectionText}>{drill.how_it_works}</Text>
        </View>

        {/* Coaching Cues */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>🎯 Coaching Cues</Text>
          {drill.coaching_cues.map((cue, index) => (
            <View key={index} style={styles.bulletItem}>
              <Text style={styles.bulletPoint}>✓</Text>
              <Text style={styles.bulletText}>{cue}</Text>
            </View>
          ))}
        </View>

        {/* Sets & Reps */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>📊 Sets & Reps</Text>
          <Text style={styles.sectionText}>{drill.sets_reps}</Text>
        </View>

        {/* Equipment */}
        {drill.equipment && drill.equipment.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>🛠️ Equipment</Text>
            <Text style={styles.sectionText}>
              {drill.equipment.join(', ')}
            </Text>
          </View>
        )}

        {/* Integration with Tools */}
        {drill.integration_with_tools && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>🔗 Tool Integration</Text>
            <Text style={styles.sectionText}>{drill.integration_with_tools}</Text>
          </View>
        )}

        {/* Expected Outcome */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>✨ Expected Outcome</Text>
          <Text style={styles.sectionText}>{drill.expected_outcome}</Text>
        </View>

        {/* Videos */}
        {drill.videos && drill.videos.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>🎥 Video Demonstrations</Text>
            {drill.videos.map((video, index) => (
              <TouchableOpacity
                key={index}
                style={styles.videoCard}
                onPress={() => handleVideoPress(video)}
              >
                <View style={styles.videoIcon}>
                  <Text style={styles.videoIconText}>▶️</Text>
                </View>
                <View style={styles.videoInfo}>
                  <Text style={styles.videoTitle}>{video.title}</Text>
                  <Text style={styles.videoDuration}>
                    {Math.floor(video.duration_seconds / 60)}:{(video.duration_seconds % 60).toString().padStart(2, '0')}
                  </Text>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  content: {
    padding: 20,
  },
  stageBadge: {
    backgroundColor: '#dbeafe',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 50,
    alignSelf: 'flex-start',
    marginBottom: 16,
  },
  stageText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#1e40af',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1e3a8a',
    marginBottom: 12,
  },
  description: {
    fontSize: 16,
    color: '#4b5563',
    lineHeight: 24,
    marginBottom: 24,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1e3a8a',
    marginBottom: 12,
  },
  sectionText: {
    fontSize: 15,
    color: '#4b5563',
    lineHeight: 22,
  },
  bulletItem: {
    flexDirection: 'row',
    marginBottom: 8,
    paddingLeft: 8,
  },
  bulletPoint: {
    fontSize: 16,
    color: '#10b981',
    fontWeight: 'bold',
    marginRight: 12,
  },
  bulletText: {
    flex: 1,
    fontSize: 15,
    color: '#4b5563',
    lineHeight: 22,
  },
  videoCard: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  videoIcon: {
    width: 60,
    height: 60,
    backgroundColor: '#dbeafe',
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  videoIconText: {
    fontSize: 28,
  },
  videoInfo: {
    flex: 1,
    justifyContent: 'center',
  },
  videoTitle: {
    fontSize: 15,
    fontWeight: '600',
    color: '#1e3a8a',
    marginBottom: 4,
  },
  videoDuration: {
    fontSize: 13,
    color: '#6b7280',
  },
});
