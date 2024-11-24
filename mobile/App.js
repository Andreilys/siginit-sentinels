import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { ThemeProvider } from 'react-native-elements';

// Screens
import LoginScreen from './screens/auth/LoginScreen';
import DashboardScreen from './screens/dashboard/DashboardScreen';
import AlertsScreen from './screens/alerts/AlertsScreen';

const Stack = createStackNavigator();

const theme = {
  colors: {
    primary: '#4a90e2',
    secondary: '#6c757d',
    success: '#28a745',
    danger: '#dc3545',
    warning: '#ffc107',
    info: '#17a2b8',
  },
};

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="Login">
          <Stack.Screen 
            name="Login" 
            component={LoginScreen}
            options={{ headerShown: false }}
          />
          <Stack.Screen 
            name="Dashboard" 
            component={DashboardScreen}
            options={{ headerLeft: null }}
          />
          <Stack.Screen 
            name="Alerts" 
            component={AlertsScreen}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </ThemeProvider>
  );
}
