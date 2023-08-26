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
    const [confirmEmail, onChangeConfirmEmail] = useState('');
    const [leaseID, onChangeLeaseID] = useState('');
    const [password, onChangePassword] = useState('');
    const [confirmPassword, onChangeConfirmPassword] = useState('');
    const [passwordError, setPasswordError] = useState('');

    const onCreateAccount = async () => {
        if (globals.backendOn) {
            try {
                
                console.log("about to fetch for create account");

                // Create account form
                const form = new FormData();
                form.append("realName", name);
                form.append("username", email);
                form.append("email", confirmEmail);
                form.append("leaseID", leaseID);
                form.append("password", password);
                form.append("confirmedPassword", confirmPassword);

                // Get response from backend
                const resp = await fetch(endpoints.registerPoint, {
                    method: 'POST',
                    body: form
                });
                const reply = await resp.json();
                
                if (reply.status == "success") {
                    console.log("success");
                    console.log(reply);          
                    
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
                    }
                
                // Account creation failed
                } else {
                    console.log("no success");
                    console.log(reply.status);
                    console.log(reply.err);
                    setPasswordError(reply.messages);
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
            onChangeText={onChangeEmail}
            placeholderTextColor="#7a7a7a"
            placeholder = "Email"
            value = {email}
            keyboardType="email-address"
          />
          <TextInput style = {styles.inputContainer}
            placeholder = "Confirm Email"
            placeholderTextColor="#7a7a7a"
            onChangeText={onChangeConfirmEmail}
            value = {confirmEmail}
            keyboardType="email-address"
          />
          <TextInput style = {styles.inputContainer}
            placeholder = "Name"
            placeholderTextColor="#7a7a7a"
            onChangeText={onChangeName}
            value = {name}
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