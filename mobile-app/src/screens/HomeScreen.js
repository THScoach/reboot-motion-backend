import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  StatusBar,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export default function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />
      
      <LinearGradient
        colors={['#1e3a8a', '#312e81']}
        style={styles.gradient}
      >
        <ScrollView contentContainerStyle={styles.scrollContent}>
          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.title}>Reboot Motion</Text>
            <Text style={styles.subtitle}>
              Biomechanics Analysis & Training Platform
            </Text>
          </View>

          {/* Main Actions */}
          <View style={styles.actionsContainer}>
            <TouchableOpacity
              style={[styles.actionCard, styles.primaryCard]}
              onPress={() => navigation.navigate('Analysis')}
            >
              <Text style={styles.actionIcon}>🎯</Text>
              <Text style={styles.actionTitle}>New Analysis</Text>
              <Text style={styles.actionDescription}>
                Get instant swing analysis with personalized recommendations
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.actionCard, styles.secondaryCard]}
              onPress={() => navigation.navigate('VideoLibrary')}
            >
              <Text style={styles.actionIcon}>🎬</Text>
              <Text style={styles.actionTitle}>Video Library</Text>
              <Text style={styles.actionDescription}>
                Browse drill demonstrations and coaching content
              </Text>
            </TouchableOpacity>
          </View>

          {/* Features */}
          <View style={styles.featuresContainer}>
            <Text style={styles.featuresTitle}>Features</Text>
            
            <View style={styles.featureItem}>
              <Text style={styles.featureIcon}>🧬</Text>
              <View style={styles.featureText}>
                <Text style={styles.featureName}>Motor Preference Detection</Text>
                <Text style={styles.featureDescription}>
                  SPINNER/GLIDER/LAUNCHER analysis
                </Text>
              </View>
            </View>

            <View style={styles.featureItem}>
              <Text style={styles.featureIcon}>📊</Text>
              <View style={styles.featureText}>
                <Text style={styles.featureName}>Fair Scoring System</Text>
                <Text style={styles.featureDescription}>
                  Motor-aware scoring adjustments
                </Text>
              </View>
            </View>

            <View style={styles.featureItem}>
              <Text style={styles.featureIcon}>⚡</Text>
              <View style={styles.featureText}>
                <Text style={styles.featureName}>Kinetic Capacity</Text>
                <Text style={styles.featureDescription}>
                  Bat speed & exit velo potential
                </Text>
              </View>
            </View>

            <View style={styles.featureItem}>
              <Text style={styles.featureIcon}>🎓</Text>
              <View style={styles.featureText}>
                <Text style={styles.featureName}>Personalized Drills</Text>
                <Text style={styles.featureDescription}>
                  Progressive training recommendations
                </Text>
              </View>
            </View>

            <View style={styles.featureItem}>
              <Text style={styles.featureIcon}>🎥</Text>
              <View style={styles.featureText}>
                <Text style={styles.featureName}>Video Demonstrations</Text>
                <Text style={styles.featureDescription}>
                  Professional coaching videos
                </Text>
              </View>
            </View>
          </View>

          {/* Footer */}
          <View style={styles.footer}>
            <Text style={styles.footerText}>
              Powered by Dr. Kwon's Biomechanics Research
            </Text>
            <Text style={styles.version}>v1.0.0</Text>
          </View>
        </ScrollView>
      </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: 40,
  },
  header: {
    paddingTop: 40,
    paddingHorizontal: 20,
    paddingBottom: 30,
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.8)',
    textAlign: 'center',
  },
  actionsContainer: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  actionCard: {
    padding: 24,
    borderRadius: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  primaryCard: {
    backgroundColor: '#fff',
  },
  secondaryCard: {
    backgroundColor: 'rgba(255,255,255,0.95)',
  },
  actionIcon: {
    fontSize: 48,
    marginBottom: 12,
  },
  actionTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#1e3a8a',
    marginBottom: 8,
  },
  actionDescription: {
    fontSize: 15,
    color: '#4b5563',
    lineHeight: 22,
  },
  featuresContainer: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  featuresTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 20,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.1)',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
  },
  featureIcon: {
    fontSize: 28,
    marginRight: 16,
  },
  featureText: {
    flex: 1,
  },
  featureName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
  },
  featureDescription: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.7)',
  },
  footer: {
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.6)',
    marginBottom: 8,
    textAlign: 'center',
  },
  version: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.4)',
  },
});
