// Example from https://reactnavigation.org/docs/bottom-tab-navigator/

import { Image, View, Text, TouchableOpacity } from 'react-native';
import colors from '../colors';

// this sets the correct icon active when selected (home, events, messages, options)
// for the navbar
const getImage = (id, active) => {
    switch (id) {
        case 'Home':
            return active ? require('../assets/Home-light.png') : require('../assets/Home-dark.png');
        case 'Tasks':
            return active ? require('../assets/Events-light.png') : require('../assets/Events-dark.png');
        case 'Roomies':
            return active ? require('../assets/Messages-light.png') : require('../assets/Messages-dark.png');
        case 'Settings':
            return active ? require('../assets/Settings-light.png') : require('../assets/Settings-dark.png');
    }
}

export default ({ state, descriptors, navigation }) => {
  return (
    <View style={{
        flexDirection: 'row',
        alignItems:"center",
        justifyContent:"space-evenly",
        borderTopLeftRadius: 10,
        borderTopRightRadius: 10,
        borderWidth: 3,
        borderColor: colors.purple,
        backgroundColor: colors.white,
        borderBottomWidth : 0,
        
    }}>
      {state.routes.map((route, index) => {
        const { options } = descriptors[route.key];
        const label =
          options.tabBarLabel !== undefined
            ? options.tabBarLabel
            : options.title !== undefined
            ? options.title
            : route.name;

        const isFocused = state.index === index;

        const onPress = () => {
          const event = navigation.emit({
            type: 'tabPress',
            target: route.key,
            canPreventDefault: true,
          });

          if (!isFocused && !event.defaultPrevented) {
            // The `merge: true` option makes sure that the params inside the tab screen are preserved
            navigation.navigate({ name: route.name, merge: true });
          }
        };

        const onLongPress = () => {
          navigation.emit({
            type: 'tabLongPress',
            target: route.key,
          });
        };

        return (
          <TouchableOpacity
            accessibilityRole="button"
            accessibilityState={isFocused ? { selected: true } : {}}
            accessibilityLabel={options.tabBarAccessibilityLabel}
            testID={options.tabBarTestID}
            onPress={onPress}
            onLongPress={onLongPress}
            style={{backgroundColor: isFocused ? colors.purple : colors.white, alignItems: "center", paddingHorizontal: 10, borderRadius: 10}}
            key={route.key}
          >
            <Image style={{width:40, height:40}} source={getImage(label, isFocused)}/>
            <Text style={{ color: isFocused ? colors.white : colors.purple }}>
              {label}
            </Text>
          </TouchableOpacity>
        );
      })}
    </View>
  );
}