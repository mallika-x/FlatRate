import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';

export default () => {
        return (
          <View style={styles.container}>
            <Text>This is the home screen! Login success</Text>
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
