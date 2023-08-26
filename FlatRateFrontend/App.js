import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'
import { StatusBar } from 'expo-status-bar'
import { SafeAreaView, Text } from 'react-native';
import { Prompt_400Regular } from '@expo-google-fonts/prompt'

// Screens
import Login from './screens/login';
import Details from './screens/details';
import CreateAccount from './screens/createAccount';
import Home from './screens/home';
import NoRoomies from './screens/noRoomies';
import Tasks from './screens/tasks';
import Settings from './screens/settings';
import Roomies from './screens/roomies';
import Notifications from './screens/notifications';
// Tabs
import NavBar from './components/NavBar'

// Fonts and colours
import { useFonts } from 'expo-font'
import colors from './colors'

// Screen Navigator
const Stack = createStackNavigator();
// Bottom tab Navigator
const Tabs = createBottomTabNavigator();


// Things in the "main app" will have the bottom navigation bar
const MainApp = () => {
  return (
    <Tabs.Navigator tabBar={NavBar} screenOptions={{headerShown:false}}>
      {/*
        Home
        Tasks
        Roomies
        Settings
      */}
      <Tabs.Screen name="Home" component={Home}/>
      <Tabs.Screen name="No Mates" component={NoRoomies}/>
      <Tabs.Screen name="Tasks" component={Tasks}/>
      <Tabs.Screen name="Roomies" component={Roomies}/>
      <Tabs.Screen name="Settings" component={Settings}/>
    </Tabs.Navigator>
  )
}

// Execution begins here
export default function App() {

  const [fontsLoaded] = useFonts({
    Prompt_400Regular, // Body
    'Sansita': require("./assets/SansitaOne-Regular.ttf") // Headings
  });

  // This displays a loading symbol until fonts have loaded
  if (!fontsLoaded) return (<><Text>loading</Text></>)

  return (
    <>
    <NavigationContainer>
        <Stack.Navigator screenOptions={{headerShown:false}}>
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="MainApp" component={MainApp} />
        <Stack.Screen name="DetailsScreen" component={Details} />
        <Stack.Screen name="CreateAccountScreen" component={CreateAccount} />
        <Stack.Screen name="NotificationsScreen" component={Notifications} />
      </Stack.Navigator>
    </NavigationContainer>
    <SafeAreaView style = {{backgroundColor: colors.white, borderWidth : 3, borderTopWidth : 0, borderColor : colors.purple}}>
    <StatusBar style="auto"/>
    </SafeAreaView>
    </>
  )
};

/*
 return (
    <>
    <NavigationContainer>
        <Stack.Navigator screenOptions={{headerShown:false}}>
        <Stack.Screen name="NavBar" component={MainApp} />
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="DetailsScreen" component={Details} />
        <Stack.Screen name="CreateAccountScreen" component={CreateAccount} />
        <Stack.Screen name="HomeScreen" component={Home} />
        <Stack.Screen name="TasksScreen" component={Tasks} />
        <Stack.Screen name="SettingsScreen" component={Settings} />
        <Stack.Screen name="RoomiesScreen" component={Roomies} />
        <Stack.Screen name="NotificationsScreen" component={Notifications} />
      </Stack.Navigator>
    </NavigationContainer>
    <SafeAreaView style = {{backgroundColor: colors.white, borderWidth : 3, borderTopWidth : 0, borderColor : colors.purple}}>
    <StatusBar style="auto"/>
    </SafeAreaView>
    </>
  )

*/