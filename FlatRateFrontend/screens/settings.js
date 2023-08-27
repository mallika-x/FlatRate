import { SafeAreaView, View } from 'react-native'
import styles from "../styles"
import IcoButton from '../components/IcoButton';
import Header from '../components/Header';
import globals from '../globals'


export default ({navigation}) => {  
  return (
    <SafeAreaView style={[styles.engageBgContainer, {justifyContent:"flex-start"}]}>
      <Header text="Options" navigation={navigation}/>
      <View style={{alignSelf: "stretch", margin: 50, justifyContent: "space-between"}}>
        <IcoButton text="Change password" onPress={() => {}} />
        <IcoButton text="Change Lease ID" onPress={() => {}} />
        <IcoButton text="View Rating" onPress={() => {}} />
        <IcoButton text="Logout" onPress={() => {globals.username=''; navigation.navigate('Login')}} />
      </View>
    </SafeAreaView>
  );
}