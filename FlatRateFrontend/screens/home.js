import React, { useState, useEffect } from 'react';
import { SafeAreaView, View, Text, TextInput, Button, StyleSheet, Image } from 'react-native';
import styles from "../styles"
import Header from '../components/Header'
import colors from '../colors'
import globals from '../globals'
import endpoints from '../endpoints';


export default () => {
    var roommatesExist = false;
    const [imageURL, setImageUrl] = useState('');

    if (globals.backendOn) {
        const [flatmateData, setData] = useState(null);
        console.log(`about to fetch flatmate data for ${globals.username}`);
        useEffect(() => {
            fetch(`${endpoints.getFlatmates}?uname=${globals.username}`)
            .then(response => response.json())
            .then(flatmateData => {
                console.log(`Response from backend: ${JSON.stringify(flatmateData)}`);
                setData(flatmateData);
            })
            .catch(error => {
              console.error('Error fetching data:', error);
            });
        }, []); // Empty dependency array ensures the effect runs once on mount

        // Get tallies image
        useEffect(() => {
            fetch(`${endpoints.getTallies}?leaseid=${globals.leaseID}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Image request failed');
                }
                return response.blob();
            })
            .then(blob => {
                // Create an object URL from the Blob
                console.log('Blob size:', blob.size);
                console.log('Blob type:', blob.type);
                const objectURL = URL.createObjectURL(blob);
                setImageUrl(objectURL);
            })
            .catch(error => {
                console.error('Error fetching image:', error);
            });
        }, []);
        
        try {
            console.log(flatmateData.emails)
            if (flatmateData.emails.length > 0) {
                roommatesExist = true;
            }
        } catch {
            console.log("Backend error")
        }
    }

    // Roommates have not registered on app
    if (!globals.backendOn || !roommatesExist) {
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
                        <Text style={{fontSize:24, fontFamily:"Sansita", color:colors.purple}}>Roommates exist.</Text>
                        <Image src={imageURL} alt="Fetched" />
                    </View>
                </SafeAreaView>
            );
    }
};

//<img src={imageURL} alt="Fetched" />
