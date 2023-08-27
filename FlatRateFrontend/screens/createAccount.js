import { useState } from 'react';
import { SafeAreaView, Text, View, TextInput, ScrollView } from 'react-native';
import PrimaryButton from '../components/PrimaryButton';
import styles from "../styles"
import globals from '../globals'
import endpoints from '../endpoints'

import { setItemAsync, getItemAsync } from 'expo-secure-store'
import colors from '../colors';

export default ({navigation}) => {
    const [name, onChangeName] = useState('');
    const [email, onChangeEmail] = useState('');
    const [address, onChangeAddress] = useState('');
    const [leaseID, onChangeLeaseID] = useState('');
    const [password, onChangePassword] = useState('');
    const [confirmPassword, onChangeConfirmPassword] = useState('');
    const [passwordError, setPasswordError] = useState('');

    const onCreateAccount = async () => {
        if (globals.backendOn) {
            try {
                
                console.log("about to fetch for create account");
                // Split names
                const names = name.split(' ');
                const firstNames = names[0]
                const surname = names[1]
                // Create account form
                const form = new FormData();
                form.append("fnames", firstNames);
                form.append("sname", surname);
                form.append("address", address);
                form.append("leaseid", leaseID);
                form.append("email", email);
                //form.append("password", password);
                //form.append("confirmedPassword", confirmPassword);

                // Get response from backend
                const resp = await fetch(endpoints.registerPoint, {
                    method: 'POST',
                    body: form
                });
                const reply = await resp.json();
                console.log(reply)
                
                if (reply[0] == "good") {
                    console.log("success");
                    navigation.navigate("MainApp");
                    /*         
                    // now we get a token and then login
                    // automatically to save the user
                    // having to do it 

                    // Login form
                    const loginForm = new FormData();
                    loginForm.append("username", email);
                    loginForm.append("password", password);
                    const loginResp = await fetch(endpoints.loginPoint, {
                        method: 'POST',
                        body : loginForm
                    });
                    const loginReply = await loginResp.json();

                    // Check if login successful
                    if (loginReply.token) {
                        await setItemAsync("authToken", loginReply.token);
                        global.token = loginReply.token;
                        navigation.navigate("HomeScreen");
                    } else { // No token recieved :(
                        console.log("why no token");
                    }*/
                
                // Account creation failed
                } else {
                    console.log("no success");
                    console.log(reply.error);
                    //console.log(reply.err);
                    //setPasswordError(reply.messages);
                }
            
            } catch (err) {
                console.log(err);
            }
        } else {
            navigation.navigate('DetailsScreen');
        }
    };


    return (
      <SafeAreaView style={styles.engageBgContainer}>
        <View style={{marginVertical:35}}>
          <Text style={{...styles.text, fontSize: 42, color : colors.purple, fontFamily:'Sansita'}}>Create Your Account</Text>
        </View>
        <ScrollView contentContainerStyle={{alignItems:"center"}}>
          <TextInput style = {styles.inputContainer}
            placeholder = "Name"
            placeholderTextColor="#7a7a7a"
            onChangeText={onChangeName}
            value = {name}
          />
          <TextInput style = {styles.inputContainer}
            onChangeText={onChangeEmail}
            placeholderTextColor="#7a7a7a"
            placeholder = "Email"
            value = {email}
            keyboardType="email-address"
          />
          <TextInput style = {styles.inputContainer}
            placeholder = "Address"
            placeholderTextColor="#7a7a7a"W
            onChangeText={onChangeAddress}
            value = {address}
          />
          <TextInput style = {styles.inputContainer}
            placeholder = "Lease ID/Bond Number"
            placeholderTextColor="#7a7a7a"
            onChangeText={onChangeLeaseID}
            value = {leaseID}
          />
          <TextInput style = {styles.inputContainer}
            placeholder = "Password"
            placeholderTextColor="#7a7a7a"
            onChangeText={onChangePassword}          
            value = {password}
            secureTextEntry={true}
          />
          <TextInput style = {styles.inputContainer}
            placeholder = "Confirm password"
            onChangeText={onChangeConfirmPassword}
            placeholderTextColor="#7a7a7a"
            value = {confirmPassword}
            secureTextEntry={true}
          />
          
          { passwordError.length > 0 &&
            <Text style = {styles.walkthroughText}>{passwordError}</Text>
          }
          <PrimaryButton text='Create' size={32} style={{width:230, height:60, marginVertical:10}} onPress = {onCreateAccount} />  
          <PrimaryButton text='Back' size={32} style={{width:230, height:60, marginVertical: 10}} onPress = {navigation.goBack} />
        </ScrollView>
        
      </SafeAreaView>
    );
  }