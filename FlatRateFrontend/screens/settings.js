import React, { useState } from 'react';
import { SafeAreaView, iew, Text, TextInput, Button, StyleSheet } from 'react-native';
import styles from "../styles"
import Header from '../components/Header'

export default ({navigation}) => {
        return (
            <SafeAreaView style={[styles.engageBgContainer, {justifyContent:"flex-start"}]}>
                <Header text="Settings" navigation={navigation} />
            </SafeAreaView>
        );
};
