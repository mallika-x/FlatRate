import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';

export default () => {
        return (
          <View style={styles.container}>
            <Text>Settings here</Text>
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
