import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';

const DetailsScreen = () => {
        return (
          <View style={styles.container}>
            <Text>Hello, World!</Text>
          </View>
    );
};
      
const styles = StyleSheet.create({
    container: {
          flex: 1,
          justifyContent: 'center',
          alignItems: 'center',
    },
});

export default DetailsScreen;