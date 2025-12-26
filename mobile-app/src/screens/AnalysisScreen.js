import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { analyzeSwing } from '../services/api';

export default function AnalysisScreen({ navigation }) {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    groundScore: '38',
    engineScore: '58',
    weaponScore: '55',
    heightInches: '68',
    wingspanInches: '69',
    weightLbs: '190',
    age: '33',
    batWeightOz: '30',
    actualBatSpeed: '67',
    rotationKE: '3743',
    translationKE: '421',
  });

  const updateField = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleAnalyze = async () => {
    // Validate required fields
    if (!formData.groundScore || !formData.engineScore || !formData.weaponScore ||
        !formData.heightInches || !formData.weightLbs || !formData.age) {
      Alert.alert('Missing Fields', 'Please fill in all required fields');
      return;
    }

    setLoading(true);

    try {
      const data = {
        groundScore: parseInt(formData.groundScore),
        engineScore: parseInt(formData.engineScore),
        weaponScore: parseInt(formData.weaponScore),
        heightInches: parseFloat(formData.heightInches),
        wingspanInches: formData.wingspanInches ? parseFloat(formData.wingspanInches) : null,
        weightLbs: parseFloat(formData.weightLbs),
        age: parseInt(formData.age),
        batWeightOz: formData.batWeightOz ? parseInt(formData.batWeightOz) : 30,
        actualBatSpeed: formData.actualBatSpeed ? parseFloat(formData.actualBatSpeed) : null,
        rotationKE: formData.rotationKE ? parseFloat(formData.rotationKE) : null,
        translationKE: formData.translationKE ? parseFloat(formData.translationKE) : null,
      };

      const result = await analyzeSwing(data);
      
      setLoading(false);
      navigation.navigate('Results', { analysisData: result.data });
    } catch (error) {
      setLoading(false);
      Alert.alert(
        'Analysis Error',
        'Failed to analyze swing. Please check your connection and try again.'
      );
      console.error('Analysis error:', error);
    }
  };

  const loadSampleData = () => {
    setFormData({
      groundScore: '38',
      engineScore: '58',
      weaponScore: '55',
      heightInches: '68',
      wingspanInches: '69',
      weightLbs: '190',
      age: '33',
      batWeightOz: '30',
      actualBatSpeed: '67',
      rotationKE: '3743',
      translationKE: '421',
    });
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.sectionTitle}>Video Analysis Scores *</Text>
        
        <View style={styles.row}>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Ground (0-100) *</Text>
            <TextInput
              style={styles.input}
              value={formData.groundScore}
              onChangeText={(v) => updateField('groundScore', v)}
              keyboardType="numeric"
              placeholder="38"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Engine (0-100) *</Text>
            <TextInput
              style={styles.input}
              value={formData.engineScore}
              onChangeText={(v) => updateField('engineScore', v)}
              keyboardType="numeric"
              placeholder="58"
            />
          </View>
        </View>

        <View style={styles.inputGroup}>
          <Text style={styles.label}>Weapon (0-100) *</Text>
          <TextInput
            style={styles.input}
            value={formData.weaponScore}
            onChangeText={(v) => updateField('weaponScore', v)}
            keyboardType="numeric"
            placeholder="55"
          />
        </View>

        <Text style={[styles.sectionTitle, styles.sectionMargin]}>
          Athlete Information *
        </Text>

        <View style={styles.row}>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Height (inches) *</Text>
            <TextInput
              style={styles.input}
              value={formData.heightInches}
              onChangeText={(v) => updateField('heightInches', v)}
              keyboardType="numeric"
              placeholder="68"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Wingspan (inches)</Text>
            <TextInput
              style={styles.input}
              value={formData.wingspanInches}
              onChangeText={(v) => updateField('wingspanInches', v)}
              keyboardType="numeric"
              placeholder="69"
            />
          </View>
        </View>

        <View style={styles.row}>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Weight (lbs) *</Text>
            <TextInput
              style={styles.input}
              value={formData.weightLbs}
              onChangeText={(v) => updateField('weightLbs', v)}
              keyboardType="numeric"
              placeholder="190"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Age *</Text>
            <TextInput
              style={styles.input}
              value={formData.age}
              onChangeText={(v) => updateField('age', v)}
              keyboardType="numeric"
              placeholder="33"
            />
          </View>
        </View>

        <View style={styles.inputGroup}>
          <Text style={styles.label}>Bat Weight (oz)</Text>
          <TextInput
            style={styles.input}
            value={formData.batWeightOz}
            onChangeText={(v) => updateField('batWeightOz', v)}
            keyboardType="numeric"
            placeholder="30"
          />
        </View>

        <Text style={[styles.sectionTitle, styles.sectionMargin]}>
          Optional Data
        </Text>

        <View style={styles.inputGroup}>
          <Text style={styles.label}>Actual Bat Speed (mph)</Text>
          <TextInput
            style={styles.input}
            value={formData.actualBatSpeed}
            onChangeText={(v) => updateField('actualBatSpeed', v)}
            keyboardType="numeric"
            placeholder="67"
          />
        </View>

        <View style={styles.row}>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Rotation KE (J)</Text>
            <TextInput
              style={styles.input}
              value={formData.rotationKE}
              onChangeText={(v) => updateField('rotationKE', v)}
              keyboardType="numeric"
              placeholder="3743"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Translation KE (J)</Text>
            <TextInput
              style={styles.input}
              value={formData.translationKE}
              onChangeText={(v) => updateField('translationKE', v)}
              keyboardType="numeric"
              placeholder="421"
            />
          </View>
        </View>

        <TouchableOpacity 
          style={styles.sampleButton}
          onPress={loadSampleData}
        >
          <Text style={styles.sampleButtonText}>
            Load Sample Data (Eric Williams)
          </Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.analyzeButton, loading && styles.analyzeButtonDisabled]}
          onPress={handleAnalyze}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.analyzeButtonText}>
              🔬 Analyze Swing
            </Text>
          )}
        </TouchableOpacity>

        <Text style={styles.footnote}>* Required fields</Text>
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
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1e3a8a',
    marginBottom: 16,
  },
  sectionMargin: {
    marginTop: 24,
  },
  row: {
    flexDirection: 'row',
    gap: 12,
  },
  inputGroup: {
    flex: 1,
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#e5e7eb',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
  sampleButton: {
    backgroundColor: '#e5e7eb',
    padding: 14,
    borderRadius: 8,
    marginTop: 8,
    marginBottom: 16,
  },
  sampleButtonText: {
    textAlign: 'center',
    fontSize: 15,
    fontWeight: '600',
    color: '#4b5563',
  },
  analyzeButton: {
    backgroundColor: '#3b82f6',
    padding: 16,
    borderRadius: 12,
    shadowColor: '#3b82f6',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  analyzeButtonDisabled: {
    backgroundColor: '#9ca3af',
  },
  analyzeButtonText: {
    textAlign: 'center',
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  footnote: {
    fontSize: 12,
    color: '#6b7280',
    textAlign: 'center',
    marginTop: 16,
    marginBottom: 40,
  },
});
