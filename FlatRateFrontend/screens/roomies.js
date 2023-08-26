import { Text, ScrollView, SafeAreaView, StyleSheet, View } from 'react-native'
import { useState, useEffect } from 'react';
import Header from '../components/Header';
import PrimaryButton from '../components/PrimaryButton';
import SecondaryButton from '../components/SecondaryButton';
import globalStyles from "../styles"
import endpoints from '../endpoints';


const styles = StyleSheet.create({
  button: {
    height:61,
    marginVertical:8
  }
});

export default ({navigation}) => {
    return (
        <SafeAreaView style={[globalStyles.engageBgContainer, {justifyContent:"flex-start"}]}>
          <Header text="Messages" navigation={navigation}/>
          <View style={{alignSelf: "stretch", margin: 50, justifyContent: "space-between"}}>
            <SecondaryButton text="Send new message" size={22} style={styles.button} onPress={() => {}} />
            <PrimaryButton text="Add new roomie" size={22} style={styles.button} onPress={() => {}} />
          </View>
        </SafeAreaView>
      );
}
