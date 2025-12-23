import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from './src/screens/HomeScreen';
import AnalysisScreen from './src/screens/AnalysisScreen';
import ResultsScreen from './src/screens/ResultsScreen';
import DrillDetailScreen from './src/screens/DrillDetailScreen';
import VideoLibraryScreen from './src/screens/VideoLibraryScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#1e3a8a',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen 
          name="Home" 
          component={HomeScreen}
          options={{ title: 'Reboot Motion' }}
        />
        <Stack.Screen 
          name="Analysis" 
          component={AnalysisScreen}
          options={{ title: 'New Analysis' }}
        />
        <Stack.Screen 
          name="Results" 
          component={ResultsScreen}
          options={{ title: 'Analysis Results' }}
        />
        <Stack.Screen 
          name="DrillDetail" 
          component={DrillDetailScreen}
          options={{ title: 'Drill Details' }}
        />
        <Stack.Screen 
          name="VideoLibrary" 
          component={VideoLibraryScreen}
          options={{ title: 'Video Library' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
