//import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import LoginScreen from './screens/login';
import Details from './screens/details';
import CreateAccount from './screens/createAccount';
import Home from './screens/home';
import { useFonts } from 'expo-font'
import { Prompt_400Regular } from '@expo-google-fonts/prompt'
import { Text } from 'react-native';


const Stack = createStackNavigator();

export default function App() {

  const [fontsLoaded] = useFonts({
    Prompt_400Regular, // Body
    'Sansita': require("./assets/SansitaOne-Regular.ttf") // Headings
  });

  // this displays a loading symbol until fonts have loaded
  if (!fontsLoaded) return (<><Text>loading</Text></>)

  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="DetailsScreen" component={Details} />
        <Stack.Screen name="CreateAccountScreen" component={CreateAccount} />
        <Stack.Screen name="HomeScreen" component={Home} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};