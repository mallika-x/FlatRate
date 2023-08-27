import React, { useState } from 'react';
import { SafeAreaView, View, Text, TextInput, Button, StyleSheet, Image } from 'react-native';
import styles from "../styles"
import Header from '../components/Header'
import colors from '../colors'
import globals from '../globals'


export default ({navigation}) => {
    if (!globals.backendOn) {
            return (
                <SafeAreaView style={[styles.engageBgContainer, {justifyContent:"flex-start"}]}>
                    <Header text="Welcome" />
                    <View style={{flexGrow: 1, alignSelf: "stretch", margin: 35, justifyContent: "space-between"}}>
                        <Text style={{fontSize:24, fontFamily:"Sansita", color:colors.purple}}>You don't have any roommates yet. Please ask your roommates to register on FlatRate using the same lease ID.</Text>
                        <View style={{margin: 75, alignItems:'center'}}>
                            <Image style={{width:200, height:200}} source={require("../assets/Flatrate_Logo.png")}/>
                        </View>
                    </View>
                </SafeAreaView>
            );
        } else {
            return (
                <SafeAreaView style={[styles.engageBgContainer, {justifyContent:"flex-start"}]}>
                    <Header text="Welcome" />
                    <View style={{flexGrow: 1, alignSelf: "stretch", margin: 35, justifyContent: "space-between"}}>
                        <Text style={{fontSize:24, fontFamily:"Sansita", color:colors.purple}}>This is different.</Text>
                    </View>
                </SafeAreaView>
            );
        }
};
